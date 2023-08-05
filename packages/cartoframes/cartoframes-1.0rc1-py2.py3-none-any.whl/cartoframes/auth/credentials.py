"""Credentials management for CARTOframes usage."""

import os
import json
import appdirs

from urllib.parse import urlparse
from carto.auth import APIKeyAuthClient
from carto.do_token import DoTokenManager

from .. import __version__
from ..utils.logger import log
from ..utils.utils import is_valid_str, check_do_enabled

from warnings import filterwarnings
filterwarnings('ignore', category=FutureWarning, module='carto')

_USER_CONFIG_DIR = appdirs.user_config_dir('cartoframes')
_DEFAULT_PATH = os.path.join(_USER_CONFIG_DIR, 'cartocreds.json')


class Credentials:
    """Credentials class is used for managing and storing user CARTO credentials. The
    arguments are listed in order of precedence: :obj:`Credentials` instances
    are first, `key` and `base_url`/`username` are taken next, and
    `config_file` (if given) is taken last. The config file is `cartocreds.json`
    by default. If no arguments are passed, then there will be an attempt to
    retrieve credentials from a previously saved session.
    One of the above scenarios needs to be met to successfully
    instantiate a :obj:`Credentials` object.

    Args:
        username (str, optional): Username of CARTO account.
        api_key (str, optional): API key of user's CARTO account. If the dataset is
            public, it can be set to 'default_public'.
        base_url (str, optional): Base URL used for API calls. This is usually
            of the form `https://johnsmith.carto.com/` for user `johnsmith`.
            On premises installations (and others) have a different URL
            pattern.
        session (requests.Session, optional): requests session. See `requests
            documentation
            <http://docs.python-requests.org/en/master/user/advanced/>`__
            for more information.

    Raises:
        ValueError: if not available `username` or `base_url` are found.

    Example:
        >>> creds = Credentials(username='johnsmith', api_key='abcdefg')

    """
    def __init__(self, username=None, api_key='default_public', base_url=None, session=None):
        if not is_valid_str(username) and not is_valid_str(base_url):
            raise ValueError('You must set at least a `username` or a `base_url` parameters')

        if base_url is not None and urlparse(base_url).scheme != 'https':
            raise ValueError('`base_url`s need to be over `https`. Update your `base_url`.')

        self._api_key = api_key
        self._username = username
        self._base_url = base_url or self._base_url_from_username()
        self._session = session
        self._api_key_auth_client = None

        self._norm_credentials()

    def __eq__(self, obj):
        return self._api_key == obj._api_key and \
               self._username == obj._username and \
               self._base_url == obj._base_url

    def __repr__(self):
        return ("Credentials(username='{username}', "
                "api_key='{api_key}', "
                "base_url='{base_url}')").format(username=self._username,
                                                 api_key=self._api_key,
                                                 base_url=self._base_url)

    @property
    def api_key(self):
        """Credentials api_key"""
        return self._api_key

    @property
    def username(self):
        """Credentials username"""
        return self._username

    @property
    def base_url(self):
        """Credentials base_url"""
        return self._base_url

    @property
    def session(self):
        """Credentials session"""
        return self._session

    @session.setter
    def session(self, session):
        """Set session"""
        self._session = session

    @classmethod
    def from_file(cls, config_file=None, session=None):
        """Retrives credentials from a file. Defaults to the user config directory.

        Args:
            config_file (str, optional): Location where credentials are loaded from.
                If no argument is provided, it will be loaded from the default location.
            session (requests.Session, optional): requests session. See `requests
                documentation
                <http://docs.python-requests.org/en/master/user/advanced/>`__
                for more information.

        Returns:
            A (:obj:`Credentials`) instance.

        Example:
            >>> creds = Credentials.from_file('creds.json')

        """
        try:
            with open(config_file or _DEFAULT_PATH, 'r') as f:
                credentials = json.load(f)
            return cls(
                credentials.get('username'),
                credentials.get('api_key'),
                credentials.get('base_url'),
                session)
        except FileNotFoundError:
            raise FileNotFoundError('There is no default credentials file. '
                                    'Run `Credentials(...).save()` to create a credentials file.')

    @classmethod
    def from_credentials(cls, credentials):
        """Retrives credentials from another Credentials object.

        Args:
            credentials (:obj:`Credentials`)

        Returns:
            A (:obj:`Credentials`) instance.

        Raises:
            ValueError: if the credentials argument is not an instance of Credentials.

        Example:
            >>> creds = Credentials.from_credentials(orig_creds)

        """
        if not isinstance(credentials, Credentials):
            raise ValueError('`credentials` must be a Credentials class instance.')
        return cls(
            credentials.username,
            credentials.api_key,
            credentials.base_url,
            credentials.session)

    def save(self, config_file=None):
        """Saves current user credentials to user directory.

        Args:
            config_file (str, optional): Location where credentials are to be
                stored. If no argument is provided, it will be send to the
                default location.

        Example:
            >>> credentials = Credentials(username='johnsmith', api_key='abcdefg')
            >>> credentials.save('creds.json')
            User credentials for `johnsmith` were successfully saved to `creds.json`

        """
        if config_file is None:
            config_file = _DEFAULT_PATH

            # create directory if not exists
            if not os.path.exists(_USER_CONFIG_DIR):
                os.makedirs(_USER_CONFIG_DIR)

        with open(config_file, 'w') as _file:
            json.dump({
                'username': self._username,
                'api_key': self._api_key,
                'base_url': self._base_url}, _file)
            log.info('User credentials for `{0}` were successfully saved to `{1}`'.format(
                self._username or self._base_url, config_file))

    @classmethod
    def delete(cls, config_file=None):
        """Deletes the credentials file specified in `config_file`. If no
        file is specified, it deletes the default user credential file
        (`cartocreds.json`)

        Args:
            config_file (str): Path to configuration file. Defaults to delete
                the user default location if `None`.

        .. Tip::

            To see if there is a default user credential file stored, do the
            following:

            >>> print(Credentials.from_file())
            Credentials(username='johnsmith', api_key='abcdefg',
            base_url='https://johnsmith.carto.com/')

        """
        path_to_remove = config_file or _DEFAULT_PATH

        try:
            os.remove(path_to_remove)
            log.info('Credentials at {} successfully removed.'.format(path_to_remove))
        except OSError:
            log.warning('No credential file found at {}.'.format(path_to_remove))

    @check_do_enabled
    def get_do_credentials(self):
        """Returns the Data Observatory v2 credentials"""
        do_token_manager = DoTokenManager(self.get_api_key_auth_client())
        return do_token_manager.get()

    def get_api_key_auth_client(self):
        if not self._api_key_auth_client:
            self._api_key_auth_client = APIKeyAuthClient(
                base_url=self._base_url,
                api_key=self.api_key,
                session=self.session,
                client_id='cartoframes_{}'.format(__version__),
                user_agent='cartoframes_{}'.format(__version__)
            )

        return self._api_key_auth_client

    def _norm_credentials(self):
        """Standardize credentials"""
        if self._base_url:
            self._base_url = self._base_url.strip('/')

    def _base_url_from_username(self):
        return 'https://{}.carto.com/'.format(self._username)

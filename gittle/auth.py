# Python imports
try:
    # Try importing the faster version
    from cStringIO import StringIO
except ImportError:
    # Fallback to pure python if not available
    from StringIO import StringIO
import os

# Paramiko imports
import paramiko

# Local imports
from gittle import utils


class GitAuthentication(object):
    KWARG_KEYS = (
        'username',
        'password',
        'pkey',
    )

    def __init__(self, username=None, password=None, pkey=None):
        self.username = username
        self.password = password
        self.pkey = self.setup_pkey(pkey)

    def get_pkey_file(self, pkey):
        if isinstance(pkey, basestring):
            if os.path.exists(pkey):
                pkey_file = open(pkey)
            else:
                # Raw data
                pkey_file = StringIO(pkey)
        else:
            return pkey
        return pkey_file

    def setup_pkey(self, pkey):
        pkey_file = self.get_pkey_file(pkey)
        if not pkey_file:
            return None
        return paramiko.RSAKey.from_private_key(pkey_file)

    @property
    def can_password(self):
        return self.username and self.password

    @property
    @utils.negate
    def can_pkey(self):
        return self.pkey is None

    def can_auth(self):
        return any([
            self.can_password,
            self.can_pkey,
        ])

    def kwargs(self):
        kwargs = {
            key: getattr(self, key)
            for key in self.KWARG_KEYS
            if getattr(self, key, None)
        }
        return kwargs

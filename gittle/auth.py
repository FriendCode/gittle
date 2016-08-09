# Copyright 2012-2013 Aaron O'Mullan <aaron.omullan@friendco.de>
#
# This program is free software; you can redistribute it and/or
# modify it only under the terms of the GNU GPLv2 and/or the Apache
# License, Version 2.0.  See the COPYING file for further details.

# Python imports
import os
try:
    # Try importing the faster version
    from io import StringIO
except ImportError:
    # Fallback to pure python if not available
    from io import StringIO


# Paramiko imports
try:
    import paramiko
    HAS_PARAMIKO = True
except ImportError:
    HAS_PARAMIKO = False

# Local imports
from .exceptions import InvalidRSAKey


# Exports
__all__ = ('GittleAuth',)

if os.sys.version_info.major > 2 or (os.sys.version_info.major == 2 and os.sys.version_info.minor < 7):
    str = str

def get_pkey_file(pkey):
    if isinstance(pkey, str):
        if os.path.exists(pkey):
            pkey_file = open(pkey)
        else:
            # Raw data
            pkey_file = StringIO(pkey)
    else:
        return pkey
    return pkey_file


class GittleAuth(object):
    KWARG_KEYS = (
        'username',
        'password',
        'pkey',
        'look_for_keys',
        'allow_agent'
    )

    def __init__(self, username=None, password=None, pkey=None, look_for_keys=None, allow_agent=None):
        self.username = username
        self.password = password
        self.allow_agent = allow_agent
        self.look_for_keys = look_for_keys

        self.pkey = self.setup_pkey(pkey)

    def setup_pkey(self, pkey):
        pkey_file = get_pkey_file(pkey)
        if not pkey_file:
            return None
        if HAS_PARAMIKO:
            return paramiko.RSAKey.from_private_key(pkey_file)
        else:
            raise InvalidRSAKey('Requires paramiko to build RSA key')

    @property
    def can_password(self):
        return self.username and self.password

    @property
    def can_pkey(self):
        return not self.pkey is None

    @property
    def could_other(self):
        return self.look_for_keys or self.allow_agent

    def can_auth(self):
        return any([
            self.can_password,
            self.can_pkey,
            self.could_other
        ])

    def kwargs(self):
        kwargs = {
            key: getattr(self, key)
            for key in self.KWARG_KEYS
            if getattr(self, key, None)
        }
        return kwargs

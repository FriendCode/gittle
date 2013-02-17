# Python imports
from urlparse import urlparse

# Local imports
from funky import first_true


def is_http_url(url, parsed):
    if parsed.scheme in ('http', 'https'):
        return parsed.scheme
    return None


def is_git_url(url, parsed):
    if parsed.scheme == 'git':
        return parsed.scheme
    return None


def is_ssh_url(url, parsed):
    if parsed.scheme == 'git+ssh':
        return parsed.scheme
    return None


def get_protocol(url):
    schemers = [
        is_git_url,
        is_ssh_url,
        is_http_url,
    ]

    parsed = urlparse(url)

    try:
        return first_true([
            schemer(url, parsed)
            for schemer in schemers
        ])
    except:
        pass
    return None


def get_password(url):
    pass


def get_user(url):
    pass


def parse_url(url, defaults=None):
    """Parse a url corresponding to a git repository
    """
    DEFAULTS = {
        'protocol': 'git+ssh',
    }
    defaults = defaults or DEFAULTS

    protocol = get_protocol() or defaults.get('protocol')

    return {
        'domain': domain,
        'protocol': protocol,
        'user': user,
        'password': password,
        'path': path,
    }


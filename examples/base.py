"""
from gittle import Gittle


def random_char():
    while True:
        yield random.choice(string.ascii_letters)

TMP_FILES = {
    'local': {
        'a'
        'b': random_content(),
    },
    'remote': {

    }

}


GIT_PATHS = {
    'remote': '/tmp/gittle_test_remote',
    'local': '/tmp/gittle_test_local',
}



def random_content(length=512):
    return ''.join([
        random.choice(string.ascii_letters)
        for x in xrange(length)
    ])


def create_remote():
    remote = Gittle.init(TMP_REMOTE_GIT)


def create_local():
    local = Gittle.init(TMP_LOCAL_GIT)
"""
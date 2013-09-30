#!/usr/bin/python

import platform
windows = platform.system() == 'Windows'
try:
    from setuptools import setup, Extension
except ImportError:
    has_setuptools = False
    from distutils.core import setup, Extension
else:
    has_setuptools = True
    if windows:
        from setuptools.command.easy_install import easy_install
        run_setup = easy_install.run_setup
        def _run_setup(self, setup_script, setup_base, args):
            """Alternate run_setup function to pass '--pure' to the Dulwich
            installer on Windows.
            """
            if 'dulwich' in setup_script:
                args.insert(0,'--pure')
            run_setup(self, setup_script, setup_base, args) 
        easy_install.run_setup = _run_setup


version_string = '0.2.2'


setup_kwargs = {}

# Requirements
install_requires = [
    # PyPi
    'paramiko==1.10.0' if not windows else '',
    'pycrypto==2.6' if not windows else '',

    # Non PyPi
    'dulwich',
    'funky',
    'mimer',
]
dependency_links = [
    'https://github.com/AaronO/dulwich/tarball/eebb032b2b7b982d21d636ac50b6e45de58b208b#egg=dulwich-0.9.1-2',
    'https://github.com/FriendCode/funky/tarball/e89cb2ce4374bf2069c7f669e52e046f63757241#egg=funky-0.0.1',
    'https://github.com/FriendCode/mimer/tarball/a812e5f631b9b5c969df5a2ea84b635490a96ced#egg=mimer-0.0.1',
]

setup(name='gittle',
    description='A high level pure python git implementation',
    keywords='git dulwich pure python gittle',
    version=version_string,
    url='https://github.com/FriendCode/gittle',
    license='MIT',
    author="Aaron O'Mullan",
    author_email='aaron@friendco.de',
    long_description="""
    Gittle is a wrapper around dulwich. It provides an easy and familiar interface to git.
    It's pure python (no dependancy on the git binary) and has no other dependancies besides
    the python stdlib, dulwich and paramiko (optional).
    """,
    packages=['gittle', 'gittle.utils'],
    install_requires=install_requires,
    dependency_links=dependency_links,
    **setup_kwargs
)

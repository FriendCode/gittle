#!/usr/bin/python

try:
    from setuptools import setup, Extension
    has_setuptools = True
except ImportError:
    from distutils.core import setup, Extension
    has_setuptools = False

version_string = '0.2.1'


setup_kwargs = {}

# Requirements
install_requires = [
    # PyPi
    'paramiko==1.10.0',
    'pycrypto==2.6',

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

#!/usr/bin/python
# Setup file for dulwich_paramiko

try:
    from setuptools import setup, Extension
    has_setuptools = True
except ImportError:
    from distutils.core import setup, Extension
    has_setuptools = False

version_string = '0.1.1'


setup_kwargs = {}

setup(name='gittle',
      description='A high level pure python git implementation',
      keywords='git dulwich pure python gittle',
      version=version_string,
      url='git+ssh://git@friendco.de:friendcode/gittle.git',
      license='MIT',
      author="Aaron O'Mullan",
      author_email='aaron.omullan@gmail.com',
      long_description="""
      Gittle is a wrapper around dulwich. It provides an easy and familiar interface to git.
      It's pure python (no dependancy on the git binary) and has no other dependancies besides
      the python stdlib, dulwich and paramiko (optional).
      """,
      packages=['gittle', 'gittle.utils'],
      **setup_kwargs
)

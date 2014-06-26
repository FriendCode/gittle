#!/usr/bin/python

"""
Setup script for Gittle.
"""

import platform
windows = platform.system() == 'Windows'
try:
    from setuptools import setup
except ImportError:
    has_setuptools = False
    from distutils.core import setup
else:
    has_setuptools = True

version_string = '0.4.0'

setup_kwargs = {
    'name': 'gittle',
    'description': 'A high level pure python git implementation',
    'keywords': 'git dulwich pure python gittle',
    'version': version_string,
    'url': 'https://github.com/FriendCode/gittle',
    'license': 'MIT',
    'author': "Aaron O'Mullan",
    'author_email': 'aaron@friendco.de',
    'long_description': """
    Gittle is a wrapper around dulwich. It provides an easy and familiar interface to git.
    It's pure python (no dependancy on the git binary) and has no other dependancies besides
    the python stdlib, dulwich and paramiko (optional).
    """,
    'packages': ['gittle', 'gittle.utils'],
    'install_requires': [
    # PyPI
    'paramiko==1.10.0',
    'pycrypto==2.6',
    'dulwich==0.9.7',
    'funky==0.0.2',
    ],
}


try:

    # Run setup with C extensions
    setup(**setup_kwargs)

except SystemExit as exc:

    import logging
    logging.exception(exc)
    logging.info("retrying installation without VisualStudio...")

    # Remove C dependencies
    install_requires = [r for r in setup_kwargs['install_requires']
                        if r.split('=')[0] not in ('paramiko', 'pycrypto')]

    # Install dulwich as pure Python
    if windows and has_setuptools:
        from setuptools.command.easy_install import easy_install
        run_setup = easy_install.run_setup

        def _run_setup(self, setup_script, setup_base, args):
            """Alternate run_setup function to pass '--pure' to the
            Dulwich installer on Windows.
            """
            if 'dulwich' in setup_script:
                args.insert(0, '--pure')
            run_setup(self, setup_script, setup_base, args)

        easy_install.run_setup = _run_setup

    # Run setup without C extensions
    setup_kwargs['install_requires'] = install_requires
    setup(**setup_kwargs)

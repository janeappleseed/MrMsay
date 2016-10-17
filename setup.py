#!/usr/bin/env python3

import os
from setuptools import setup

here = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(here, 'src', 'mrmsay', '__version__.py')) as fp:
    exec(fp.read())

setup(
    name='MrMsay',
    version=__version__,
    description="MrM's wisdom in your terminal",
    long_description='Listen to what MrM has to say.',
    url='https://github.com/janeappleseed/MrMsay',
    author='Jane Appleseed',
    email='janeappleseedgh@gmail.com',
    license='WTFPL',
    packages=['mrmsay'],
    package_dir={'': 'src'},
    install_requires=[
        'arrow>=0.8.0',
        'daemonize>=2.4.7',
        'peewee>=2.8.5',
        'requests>=2.11.1',
        'sh>=1.11',
    ],
    entry_points={
        'console_scripts': [
            'mrmd=mrmsay.daemon:main',
            'mrmsay=mrmsay.cli:main',
        ],
    },
)

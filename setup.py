from setuptools import setup

from sys import version
if version < '2.6.0':
    raise Exception("This module doesn't support any version less than 2.6")

import sys
sys.path.append("./test")

with open('README.rst', 'r') as f:
    long_description = f.read()

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    "Programming Language :: Python",
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Topic :: Software Development :: Libraries :: Python Modules'
]


setup(
    author='Keita Oouchi',
    author_email='keita.oouchi@gmail.com',
    url = 'https://github.com/keitaoouchi/easyimap',
    name = 'easyimap',
    version = '0.1.2',
    package_dir={"":"src"},
    packages = ['easyimap'],
    test_suite = "test_seleniumwrapper.suite",
    license='BSD License',
    classifiers=classifiers,
    description = 'imap wrapper for me.',
    long_description=long_description,
)

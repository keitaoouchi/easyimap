from setuptools import setup

from sys import version
if version < '2.6.0':
    raise Exception("This module doesn't support any version less than 2.6")

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
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

requires = ['chardet>=2.3.0']

setup(
    author='Menno van Hout',
    author_email='menno.vanhout@universal-games.nl',
    url='https://github.com/UGxMvH/easyimap',
    name='easyimap-python',
    version='0.6.4',
    package_dir={"easyimap-python": "easyimap-python"},
    packages=['easyimap-python'],
    license='BSD License',
    classifiers=classifiers,
    description='Simple imap wrapper.',
    long_description=long_description,
    install_requires=requires,
)

from setuptools import setup

from sys import version
if version < '2.7.0':
    raise Exception("This module doesn't support any version less than 2.7")

with open('README.rst', 'r') as f:
    long_description = f.read()

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    "Programming Language :: Python",
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

requires = ['chardet>=2.3.0']

setup(
    author='Keita Oouchi',
    author_email='keita.oouchi@gmail.com',
    url='https://github.com/keitaoouchi/easyimap',
    name='easyimap',
    version='0.7.0',
    package_dir={"easyimap": "easyimap"},
    packages=['easyimap'],
    license='BSD License',
    classifiers=classifiers,
    description='Simple imap wrapper.',
    long_description=long_description,
    install_requires=requires,
)

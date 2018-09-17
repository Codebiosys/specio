import os
import re
from setuptools import find_packages, setup


def packages(path):
    """Simple parser for requirements.txt files"""
    with open(path) as requirements:
        for line in requirements:
            if re.match('^[a-zA-Z]', line):
                yield line.strip()


def read(path):
    """ Read entire file contents and return them """
    with open(path) as fp:
        return fp.read()


HERE = os.path.dirname(__file__)
README = read(os.path.join(HERE, 'README.md'))
REQUIREMENTS = list(packages(os.path.join(HERE, 'requirements.txt')))
DEVELOPMENT = list(packages(os.path.join(HERE, 'requirements-development.txt')))

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='dom2fixture',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='A command line tool for converting DOM into a VeriPy fixtures',
    long_description=README,
    url='https://github.com/Codebiosys/specio_app',
    author='CodeBiosys, Inc',
    author_email='developers@codebiosys.com',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=REQUIREMENTS,
    extras_require={'develop': DEVELOPMENT},
    tests_require=DEVELOPMENT,
    scripts=('bin/dom2fixture',),
)

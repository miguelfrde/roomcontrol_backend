from setuptools import setup, find_packages
import os

from pip.req import parse_requirements

import roomcontrol


def read(filename):
    with open(filename, 'r') as f:
        return f.read()


def requirements(reqs_filename):
    reqs = parse_requirements(reqs_filename, session=False)
    return [str(r.req) for r in reqs]


DESCRIPTION = """
Backend service designed to run on a RaspberryPi for the RoomControl app
(https://github.com/miguelfrde/roomcontrol).
"""


setup(
    name='roomcontrol',
    version=roomcontrol.__version__,
    url='https://github.com/miguelfrde/roomcontrol_backend',
    license='MIT License',
    author='Miguel Flores Ruiz de Eguino <miguelfrde>',
    author_email='miguel.frde@gmail.com',
    description=DESCRIPTION,
    long_description=read('README.md'),
    packages=find_packages(exclude=['test', 'test.*']),
    include_package_data=True,
    platforms='any',
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python 2.7',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 1 - Planning',
        'Natural Language :: English',
        'Environment :: Other Environment',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Topic :: Utilities'
    ],
    entry_points={
        'console_scripts': [
            'roomcontrol = roomcontrol.roomcontrol:main'
        ]
    },
    tests_require=requirements('requirements-dev.txt'),
    install_requires=requirements('requirements.txt'),
    extras_require={
        'dev': requirements('requirements-dev.txt')
    }
)

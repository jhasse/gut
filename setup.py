from setuptools import setup

from gut import VERSION

setup(
    name='gut',
    version=VERSION,
    author="Jan Niklas Hasse",
    author_email="jhasse@bixense.com",
    url="https://bixense.com/gut",
    download_url='https://github.com/jhasse/gut/archive/v{}.tar.gz'.format(VERSION),
    description="User-friendly CLI frontend for Git",
    packages=['gut'],
    entry_points={
        'console_scripts': ['gut = gut.__main__:main'],
    },
    install_requires=[
        'click',
    ],
)

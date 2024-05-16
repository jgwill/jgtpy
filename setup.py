#!/usr/bin/env Python
"""
jgtpy
"""

from setuptools import find_packages, setup

#from jgtpy import __version__ as version
def read_version():
    with open("jgtpy/JGTCore.py") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.strip().split()[-1][1:-1]

version = read_version()


setup(
    name="jgtpy",
    version=version,
    description="JGTrading Data maker' Dataframes",
    long_description=open("README.rst").read(),
    author="GUillaume Isabelle",
    author_email="jgi@jgwill.com",
    url="https://github.com/jgwill/jgtpy",
    packages=find_packages(
        include=["jgtpy", "test-*.py"], exclude=["test*log", "*test*csv", "*test*png"]
    ),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.7.16",
    ],
)

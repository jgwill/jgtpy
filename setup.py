#!/usr/bin/env Python
"""
jgtpy
"""

from setuptools import find_packages, setup

import re

def read_version():
    with open("jgtpy/__init__.py") as f:
        content=f.read()
        version_match = re.search(r"version=['\"]([^'\"]*)['\"]", content)
        return version_match.group(1)

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

#!/usr/bin/env Python
"""
jgtpy
"""

from setuptools import find_packages, setup
import re
from pathlib import Path

def read_version():
    """Read version from __init__.py without importing."""
    init_file = Path(__file__).parent / "jgtpy" / "__init__.py"
    if not init_file.exists():
        return "0.0.0"
    content = init_file.read_text()
    # Try different version patterns
    for pattern in [r'version\s*=\s*["\']([^"\']+)["\']', r'__version__\s*=\s*["\']([^"\']+)["\']']:
        match = re.search(pattern, content)
        if match:
            return match.group(1)
    return "0.0.0"

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

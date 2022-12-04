#!/usr/bin/env Python
"""
jgtpy
"""

from setuptools import find_packages, setup

from jgtpy import __version__ as version

INSTALL_REQUIRES = [
    'pandas>=0.25.1',
    'fxcmpy>=1.3.3', 
]

EXTRAS_DEV_LINT = [
    "flake8>=3.6.0,<3.7.0",
    "isort>=4.3.4,<4.4.0",
]

EXTRAS_DEV_TEST = [
    "coverage",
    "pytest>=3.10",
]

EXTRAS_DEV_DOCS = [
    "readme_renderer",
    "sphinx",
    "sphinx_rtd_theme>=0.4.0",
]

setup(
    name='jgtpy',
    version=version,
    description='JGTrading Data maker\' Dataframes',
    long_description=open('README.rst').read(),
    author='GUillaume Isabelle',
    author_email='jgi@jgwill.com',
    url='https://github.com/jgwill/jgtpy',
    packages=find_packages(exclude=['*test*']),
    install_requires=INSTALL_REQUIRES,
    extras_require={
        'dev': (EXTRAS_DEV_LINT + EXTRAS_DEV_TEST + EXTRAS_DEV_DOCS),
        'dev-lint': EXTRAS_DEV_LINT,
        'dev-test': EXTRAS_DEV_TEST,
        'dev-docs': EXTRAS_DEV_DOCS,
    },
    license='MIT',
    keywords='trading',
    classifiers=[
        "Development Status :: 5 - Production/Stable", 
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent", 
        "Topic :: Software Development :: Libraries :: Python Modules", 
        "Programming Language :: Python :: 3.7", 
    ],
)

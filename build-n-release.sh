#!/bin/bash
. _version_sed.sh
make dist
twine upload dist/*
make clean

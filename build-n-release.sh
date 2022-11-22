#!/bin/bash
make dist
twine upload dist/*
make clean

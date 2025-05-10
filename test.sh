#!/bin/sh
cd src
mypy *.py
python -m unittest

#!/bin/bash

export PYTHONPATH="${PWD}/src${PYTHONPATH:+:${PYTHONPATH}}";

python -m unittest discover test -v

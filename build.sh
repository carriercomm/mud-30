#!/bin/bash
set -e
python ~/.pyenv/versions/3.4.1/bin/pep8 mud_backend/migrations/0002_auto_20151128_1652.py mud_backend/*.py

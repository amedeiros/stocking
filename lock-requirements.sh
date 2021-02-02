#!/usr/bin/env bash

pip uninstall -y -r <(pip freeze)
pip install -r requirements.txt
printf "# AUTO GENERATED LOCKFILE. DO NOT EDIT MANUALLY.\n" > requirements.lock
pip freeze --disable-pip-version-check --all >> requirements.lock

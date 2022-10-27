#!/bin/bash
python -m venv .venv;
source .venv/bin/activate;
pip install pip --upgrade;
pip install pre-commit;
pre-commit install;
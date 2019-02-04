#!/bin/bash
echo 'Testing lambda'
source venv/bin/activate
python-lambda-local -f lambda_handler lambda_function.py event.json -t 60
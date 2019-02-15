#!/usr/bin/env bash
cp lambda_function.py Lambda_package
cp Reddit.py Lambda_package
cp Account.py Lambda_package
cp praw.ini Lambda_package
cp -r venv/lib/python3.6/site-packages/* Lambda_package
cd Lambda_package
zip -r9 ~/package.zip .
aws lambda update-function-code --function-name invest_bot --zip-file fileb://~/package.zip
rm -rf ./*
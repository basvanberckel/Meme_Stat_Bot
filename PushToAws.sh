#!/usr/bin/env bash
cp *.py Lambda_package
pip install  -r requirements.txt -t Lambda_package -q
cd Lambda_package
zip -uq -r9 ~/package.zip .
aws lambda update-function-code --function-name invest_bot --zip-file fileb://~/package.zip
rm -rf ./*
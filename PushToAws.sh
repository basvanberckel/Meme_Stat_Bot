#!/usr/bin/env bash
cp *.py Lambda_package
cp model.joblib Lambda_package
echo installing dependencies
pip install  -r requirements.txt -t Lambda_package --no-cache-dir --compile -q
cd Lambda_package
rm -rf ./AI.py
echo zipping packages
zip -uq -r9 ./package.zip .
#echo pushing to aws
aws s3 cp package.zip s3://stat-bot-src/package.zip
aws lambda update-function-code --function-name stat_bot --s3-bucket stat-bot-src --s3-key package.zip
rm -rf ./*
#rm -rf ~/package.zip
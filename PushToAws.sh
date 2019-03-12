#!/usr/bin/env bash
cp *.py Lambda_package
cp model.joblib Lambda_package
echo installing dependencies
pip install  -r requirements.txt -t Lambda_package --no-cache-dir --compile -q
cd Lambda_package
echo zipping packages
zip -uq -r9 ./package.zip .
#echo pushing to aws
aws s3 cp package.zip s3://bot-src/package.zip
aws lambda update-function-code --function-name invest_bot --s3-bucket bot-src --s3-key package.zip
rm -rf ./*
#rm -rf ~/package.zip
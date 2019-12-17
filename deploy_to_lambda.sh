#!/bin/bash

zip -r package.zip lambda_function.py lib/ src/ && \
aws lambda update-function-code \
    --function-name dailyDoug \
    --zip-file fileb://./package.zip  \
    --profile optate \
    --region us-east-2

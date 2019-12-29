#!/bin/bash

zip -r package.zip lambda-daily_doug.py lib/ src/ && \
aws lambda update-function-code \
    --function-name dailyDoug \
    --zip-file fileb://./package.zip  \
    --profile optate \
    --region us-east-2

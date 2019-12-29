#!/bin/bash

zip -r package.zip lambda-untappd_api.py lib/ src/ && \
aws lambda update-function-code \
    --function-name untappdApi \
    --zip-file fileb://./package.zip  \
    --profile optate \
    --region us-east-2

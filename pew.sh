#!/bin/bash
last_checkin_id=$(cat /root/daily_lambdoug/response.json | jq '.last_checkin_id')
echo $last_checkin_id
aws lambda invoke --function-name dailyDoug --payload '{"latest_checkin_id": '"$last_checkin_id"'}' /root/daily_lambdoug/response.json

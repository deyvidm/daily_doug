import datetime
import json
import logging
import re
import requests
import yaml
import os
import functools

from bs4 import BeautifulSoup, SoupStrainer
from collections import defaultdict
from scraper import * 
from slack import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    # response = get_page(os.environ['untappd_url'])
    # checkins = gather_checkins(response)

    payload = {
        'some_val': 'test',
        'untappd_url': os.environ['untappd_url'],
        'webhook': os.environ['webhook_url']
    }

    return {
        'statusCode': 200,
        'body': json.dumps(payload),
        'last_checkin_id': 123,
    }


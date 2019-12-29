import datetime
import functools
import json
import logging
import os
import re
import sys

from collections import defaultdict

sys.path.insert(1, './lib')
sys.path.insert(1, './src')

from lib.bs4 import BeautifulSoup, SoupStrainer
from lib import pymysql
from lib import requests
from lib import yaml


from scraper import * 
from slack import *
from untappd_api import *



logging.basicConfig(
    filename=LOG_PATH, format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info("=== Run started ===")
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):

    if not event['queryStringParameters'] or not event['queryStringParameters']['beercode']:
        return {
            'statusCode': 400,
            'msg': 'Did not get beercode',
            'event': event
        }
    
    beercode = event['queryStringParameters']['beercode']
    beer = fetchBeerInfo(beercode)
    beer_info = fetchDougBeerInfo(beer['beer_slug'])
    checkin_review = fetchCheckinReview(beer_info['recent_checkin_id'])

    return {
        'statusCode': 200,
        'body': json.dumps({
            'beer': beer,
            'beer_info': beer_info,
            'review': checkin_review
        })
    }

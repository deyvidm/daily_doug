import datetime
import functools
import json
import logging
import os
import pprint
import re
import sys

from collections import defaultdict

sys.path.insert(1, './lib')
sys.path.insert(1, './src')


from lib import yaml
from lib import requests
from lib import pymysql
from lib.bs4 import BeautifulSoup, SoupStrainer

from scraper import *
from slack import *

from untappd_api import *


pp = pprint.PrettyPrinter(indent=3)

beer = fetchBeerInfo('0062067313356')
# pp.pprint(beer)
# print("===")
beer_info = fetchDougBeerInfo(beer['beer_slug'])
pp.pprint(beer_info)
checkin_review = fetchCheckinReview(beer_info['recent_checkin_id'])
print(checkin_review)

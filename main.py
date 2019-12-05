#!/usr/bin/python3

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

from slack import *
from scraper import *

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

CONFIG_PATH = os.path.join(__location__, './config.yml')
LOG_PATH = os.path.join(__location__, './runlog')

logging.basicConfig(
    filename=LOG_PATH, format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info("=== Run started ===")

config = import_config(CONFIG_PATH)
response = get_page(config['untappd_url'])
checkins = gather_checkins(response)


# Testing Code: Phase out in favour of something more flexible

# test_soup = BeautifulSoup(get_test_checkin(), 'html.parser')
# checkins = test_soup.find_all(id=re.compile(r"^checkin_\d+$"))
# config['last_checkin_id'] = '123'


slackblock_stack = []
# the checkins are fetched latest -> oldest
# > clean checkin data
# > store the first checkin's id as 'latest' -- this is the latest checkin reported by untappd
# > if the current checkin's id is the same as the one from last run, then we've run out of new checkins
# > if the previous is true, AND the current checkin's id is the same as the 'latest' checkin's id, then there are no new checkins at all
#   > just terminate, no work left to do
# > else, store the ID and finish sending the remaining new checkins
# > store the latest checkin ID and move on

# in order to display them in the right order, the list needs to be reversed
# also need to store the latest checkin's id for next run, which is easier when it's at index [0]

# fetch checkins in default untappd order (latest -> oldest)
latest_checkin_id = None
for i, c in enumerate(checkins):
    clean_checkin = scrape_checkin(c)

    if i == 0:
        latest_checkin_id = clean_checkin['checkin_id']

    if clean_checkin['checkin_id'] == config['last_checkin_id']:
        if clean_checkin['checkin_id'] == latest_checkin_id:
            logging.info("no new checkins")
            exit()
        # write_latest_checkin_id(latest_checkin_id)
        break

    # convert to slack message blocks
    slackblock_stack.append(build_slackblock(clean_checkin))

# reverse and continue
slackblock_stack.reverse()

for c in slackblock_stack:
    post_to_webhook(config['webhook_url'], json.dumps(c))

write_latest_checkin_id(latest_checkin_id, config)

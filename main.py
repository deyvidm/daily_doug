#!/usr/bin/python3

import datetime
import json
import logging
import re
import requests
import yaml
import os

from bs4 import BeautifulSoup, SoupStrainer
from collections import defaultdict

from test_cases import get_test_checkin




__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

CONFIG_PATH = os.path.join(__location__, './config.yml')
LOG_PATH =    os.path.join(__location__, './runlog')

logging.basicConfig(filename=LOG_PATH, format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info("=== Run started ===")

def post_to_webhook(webhook_url: str, json_payload: str):
    headers = {'Content-type': 'application/json'}
    r = requests.post(webhook_url, headers=headers, data=json_payload)
    logging.info("{} :: {}".format(r.status_code, r.text))

def build_slackblock_link(text: str, link: str) -> str:
    return '<{0}|{1}>'.format(link, text)

def build_slackblock_description(checkin): 
    parts = [
        build_slackblock_link(checkin['user']['text'], checkin['user']['link']) + " is drinking a ",
        build_slackblock_link(checkin['brew']['text'], checkin['brew']['link']) + " by ",
        build_slackblock_link(checkin['brewery']['text'], checkin['brew']['link'])
    ]

    if 'location' in checkin:
        parts.extend([" at ", build_slackblock_link(checkin['location']['text'], checkin['location']['link'])])
    
    return ''.join(parts)
    
def build_slackblock(clean_checkin_data): 
    blocks = defaultdict(list)
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": build_slackblock_description(clean_checkin_data) 
            }
        },{
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Rating*\n" + clean_checkin_data['rating']
                }
            ]
        },{
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": clean_checkin_data['comment']
            }
	    }
    ]

    if clean_checkin_data['image'] is not None:
        blocks.append(
        {
            "type": "image",
            "image_url": clean_checkin_data['image'],
            "alt_text": "Today's Daily Doug Brew of Day"
        }
    )

    blocks.append(
        {
            "type": "divider"
        }
    )

    return {"blocks": blocks}


def prepend_hostname(path: str) -> str:
    return "https://untappd.com" + path

def find_rating_in_class_list(classes: list) -> str:    
    r = re.compile(r'r(\d)(\d\d)')

    for c in classes: 
        m = r.match(c)
        if not m:
            continue
        
        return(m.group(1)+"."+m.group(2))

    raise Exception("could not find rating in classlist: [{}]".format(', '.join(classes)))

def scrape_checkin(checkin_container) -> dict:
    checkin_id = checkin_container['data-checkin-id']
    logging.info("processing checkin {}".format(checkin_id))

    raw_checkin_data = checkin_container.find('div', class_='checkin').find('div', class_='top')

    comment = raw_checkin_data.find('div', class_='checkin-comment').find('p', class_='comment-text').text
    rating_classes = raw_checkin_data.find('span', class_='rating')['class']
    rating = find_rating_in_class_list(rating_classes)

    raw_description_parts = raw_checkin_data.find('p', class_='text').find_all('a')

    # some posts have no image ¯\_(ツ)_/¯
    # just try and catch the AttributeError that comes from the chained .find method
    # pretty bad to actively rely on an exception -- should change this lol
    img_url = None
    try:
        img_url = raw_checkin_data.find('p', class_='photo').find('img', class_='lazy')['data-original']
    except AttributeError:
        logging.info("could not find image for {}".format(checkin_id))


    checkin = {
        'user': {
            'text': raw_description_parts[0].text,
            'link': prepend_hostname(raw_description_parts[0].get('href'))
        },
        'brew': {
            'text': raw_description_parts[1].text,
            'link': prepend_hostname(raw_description_parts[1].get('href'))
        },
        'brewery': {
            'text': raw_description_parts[2].text,
            'link': prepend_hostname(raw_description_parts[2].get('href'))
        },
        'comment': comment,
        'rating': rating,
        'image': img_url,
        'checkin_id': checkin_id
    }

    if len(raw_description_parts) == 4:
        checkin['location'] = {
            'text': raw_description_parts[3].text,
            'link': prepend_hostname(raw_description_parts[3].get('href'))
        }

    return checkin

def import_config(config_path: str) -> object:
    f = open(config_path, 'r')
    config = yaml.safe_load(f)
    return config

def get_page(url: str) -> requests.Response: 
    headers={'User-agent': 'Need my fix of Daily Doug'}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        r.raise_for_status()
    return r

def gather_checkins(http_response_obj: requests.Response) :
    soup = BeautifulSoup(http_response_obj.content, 'html.parser')
    return soup.find_all(id=re.compile(r"^checkin_\d+$"))

def write_latest_checkin_id(latest_checkin_id):
    config['last_checkin_id'] = latest_checkin_id
    with open(CONFIG_PATH, 'w') as outfile:
        yaml.dump(config, outfile, default_flow_style=False)

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
        write_latest_checkin_id(latest_checkin_id)
        break
    
    # convert to slack message blocks
    slackblock_stack.append(build_slackblock(clean_checkin))    

# reverse and continue
slackblock_stack.reverse()

for c in slackblock_stack:
    post_to_webhook(config['webhook_url'], json.dumps(c))
    
write_latest_checkin_id(latest_checkin_id)
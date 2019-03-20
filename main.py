import json
import re
import requests
import yaml
from bs4 import BeautifulSoup

def post_to_webhook(webhook_url: str, json_payload: str):
    headers = {'Content-type': 'application/json'}
    r = requests.post(webhook_url, headers=headers, data=json_payload)
    print(r.status_code)
    print(r.text)

def build_slackblock_link(text: str, link: str) -> str:
    return '<{0}|{1}>'.format(link, text)

def build_slackblock_description(checkin): 
    return ''.join([
        build_slackblock_link(checkin['user']['text'], checkin['user']['link']) + " is drinking a ",
        build_slackblock_link(checkin['brew']['text'], checkin['brew']['link']) + " by ",
        build_slackblock_link(checkin['brewery']['text'], checkin['brew']['link']) + " at ",
        build_slackblock_link(checkin['location']['text'], checkin['location']['link']),
    ])
    
def build_slackblock(clean_checkin_data): 
    return {"blocks": [
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
	    },{
            "type": "image",
            "image_url": clean_checkin_data['image'],
            "alt_text": "Today's Daily Doug Brew of Day"
        },
    ]}

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
    raw_checkin_data = checkin_container.find('div', class_='checkin').find('div', class_='top')

    raw_description_parts = raw_checkin_data.find('p', class_='text').find_all('a')
    comment = raw_checkin_data.find('div', class_='checkin-comment').find('p', class_='comment-text').text
    rating_classes = raw_checkin_data.find('span', class_='rating')['class']
    rating = find_rating_in_class_list(rating_classes)
    img_url = raw_checkin_data.find('p', class_='photo').find('img', class_='lazy')['data-original']
    
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
        'location': {
            'text': raw_description_parts[3].text,
            'link': prepend_hostname(raw_description_parts[3].get('href'))
        },
        'comment': comment,
        'rating': rating,
        'image': img_url
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

config = import_config('config.yml')
response = get_page(config['untappd_url'])
checkins = gather_checkins(response)
checkin = scrape_checkin(checkins[0])

print(checkin)

block = build_slackblock(checkin)
# print(json.dumps(block))

post_to_webhook(config['webhook_url'], json.dumps(block))
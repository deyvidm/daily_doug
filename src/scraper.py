import functools
import logging
import os
import re
import requests
import yaml


from bs4 import BeautifulSoup, SoupStrainer

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

CONFIG_PATH = os.path.join(__location__, './config.yml')
LOG_PATH = os.path.join(__location__, './runlog')

logging.basicConfig(
    filename=LOG_PATH, format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info("=== Run started ===")

class checkin_info:
    def __init__(self):
        self.review = ''

def prepend_hostname(path: str) -> str:
    return "https://untappd.com" + path


def find_rating_in_class_list(classes: list) -> str:
    r = re.compile(r'(\d)(\d\d)')

    for c in classes:
        m = r.search(c)
        if not m:
            continue

        return(m.group(1)+"."+m.group(2))

    raise Exception(
        "could not find rating in classlist: [{}]".format(', '.join(classes)))

def scrape_checkin_date(checkin_container) -> dict:
    feedback = checkin_container.find(
        'div', class_='checkin').find('div', class_='feedback')
    date = feedback.find('a').text
    return date


def scrape_checkin_review(http_response_obj: requests.Response):
    checkin_info = []
    soup = BeautifulSoup(http_response_obj.content, 'html.parser')
    find_all_result = soup.find_all(id=re.compile(r"^translate_\d+$"))
    if (len(find_all_result) != 1):
        print("found {} comments on page.".format(len(find_all_result)))
        return None
    node = find_all_result[0]
    
    return node.text.strip()



def scrape_checkin(checkin_container) -> dict:
    checkin_id = checkin_container['data-checkin-id']
    logging.info("processing checkin {}".format(checkin_id))

    raw_checkin_data_top = checkin_container.find(
        'div', class_='checkin').find('div', class_='top')

    comment = raw_checkin_data_top.find(
        'div', class_='checkin-comment').find('p', class_='comment-text').text

    rating_blob = raw_checkin_data_top.find('div', class_='caps')
    rating = 'N/A'
    if rating_blob is not None:
        rating = rating_blob['data-rating']

    raw_description_parts = raw_checkin_data_top.find(
        'p', class_='text').find_all('a')

    # some posts have no image ¯\_(ツ)_/¯
    # just try and catch the AttributeError that comes from the chained .find method
    # pretty bad to actively rely on an exception -- should change this lol
    img_url = None
    try:
        img_url = raw_checkin_data_top.find('p', class_='photo').find(
            'img', class_='lazy')['data-original']
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
        'checkin_id': checkin_id,
        'date': scrape_checkin_date(checkin_container)
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
    headers = {'User-agent': 'Need my fix of Daily Doug'}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        r.raise_for_status()
    return r


def gather_checkins(http_response_obj: requests.Response):
    soup = BeautifulSoup(http_response_obj.content, 'html.parser')
    return soup.find_all(id=re.compile(r"^checkin_\d+$"))


def write_latest_checkin_id(latest_checkin_id, config):
    config['last_checkin_id'] = latest_checkin_id
    with open(CONFIG_PATH, 'w') as outfile:
        yaml.dump(config, outfile, default_flow_style=False)


def logtest(l):
    logging.info("test")


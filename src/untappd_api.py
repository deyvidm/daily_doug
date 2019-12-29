import requests
import os

import scraper


def fetchBeerInfo(barcode): 
    url = "https://api.untappd.com/v4/beer/checkbarcodemultiple?&access_token={}&upc={}".format(
        os.environ['untappd_access_token'],
        barcode
    )
    resp = requests.get(url)
    resp.raise_for_status()

    beer = list.pop(resp.json()['response']['items'])['beer']
    return beer


def fetchDougBeerInfo(beer_slug):
    url = "https://api.untappd.com/v4/user/beers/doug1516?access_token={}&q={}".format(
        os.environ['untappd_access_token'],
        beer_slug
    )
    resp = requests.get(url)
    resp.raise_for_status()

    beer = list.pop(resp.json()['response']['beers']['items'])
    return beer

def fetchCheckinReview(checkinId):
    url = "https://untappd.com/user/doug1516/checkin/{}".format(checkinId)
    resp = requests.get(url, headers={'User-agent': 'catch me if you can, dirtbags'})
    resp.raise_for_status()

    return scraper.scrape_checkin_review(resp)


import requests
import os

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
    return beer['rating_score']

'''
    fetchDetailedCheckin = async (checkinId) => {
        return fetch('https://untappd.com/user/doug1516/checkin/' + checkinId)
            .then((response) => { 
                return response.text()
            }).then((html) => {
                var doc = this.domParser.parse(html)
                doc.getElementsByClassName('caps')
            })
    }

}

'''

import functools
import logging
import re
import requests

from collections import defaultdict


def scan_for_special_brew(checkin, blocks):
    if ('born to be mild' in checkin['brew']['text'].lower() and
            'stack brewing' in checkin['brewery']['text'].lower()):

        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "🍺 🎉 🎉 This is our friend Christina's beer! 🎉 🎉 🍺"
            }
        })

    return blocks


def post_to_webhook(webhook_url: str, json_payload: str):
    headers = {'Content-type': 'application/json'}
    r = requests.post(webhook_url, headers=headers, data=json_payload)
    logging.info("{} :: {}".format(r.status_code, r.text))


def build_slackblock_link(text: str, link: str) -> str:
    return '<{0}|{1}>'.format(link, text)


def build_slackblock_description(checkin):
    parts = [
        build_slackblock_link(
            checkin['user']['text'], checkin['user']['link']) + " is drinking a ",
        build_slackblock_link(
            checkin['brew']['text'], checkin['brew']['link']) + " by ",
        build_slackblock_link(
            checkin['brewery']['text'], checkin['brew']['link'])
    ]

    if 'location' in checkin:
        parts.extend([" at ", build_slackblock_link(
            checkin['location']['text'], checkin['location']['link'])])

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
        }, {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Rating*\n" + clean_checkin_data['rating']
                }
            ]
        }, {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": clean_checkin_data['comment']
            }
        }
    ]

    blocks = scan_for_special_brew(clean_checkin_data, blocks)

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
    
    # 🤢
    return {
        "blocks": blocks,
        "text": functools.reduce(lambda p, n: n if n < p else p, filter(lambda a: len(a), re.split('[!?.]', clean_checkin_data['comment'])))
    }


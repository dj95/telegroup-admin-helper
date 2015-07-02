#!/bin/env python3
#
# telegram admin helper
#
# © 2015 Daniel Jankowski
# Licensed under the LGPLv3

import urllib.request
import json
import time
import argparse

INTERVAL = 5 # interval before getting new updates

NOTIFY_CHAT_ID = '' # chat id of group or user, who should receive the notification
WATCH_ID = '' # chat id of group chat to watch
BANNED_NICK_NAMES = [''] # banned nicknames

TOKEN = '' # access token for your bot
BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/' # base url for bots (DON'T CHANGE!)


def get_updates(url):
    old_update_id = 0
    while True:
        rqst = urllib.request.urlopen(url)
        data = json.loads(rqst.read().decode('utf-8'))
        for i in range(len(data['result'])):
            msg = data['result'][i]
            if (msg['message']['chat']['id'] == WATCH_ID):
                if (msg['message']['chat']['from']['username'] in BANNED_NICK_NAMES):
                    if (msg['update_id'] > old_update_id):
                        send_notification('WARNING: ' + msg['message'][' chaat']['from']['username'] + 'rejoined Group' + msg['message']['chat']['title'])
                        old_update_id = msg['update_id']
        time.sleep(INTERVAL)


def send_notification(notification):
    msg = 'chat_id=' + NOTIFY_CHAT_ID + '&text=' + notification
    rqst = urllib.request.urlopen(BASE_URL + 'sendMessage', msg.encode('utf-8'))
    data = json.loads(rqst.read().decode('utf-8'))


def main():
    # arg parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('--to', type=str)
    parser.add_argument('--token', type=str)
    parser.add_argument('--interval', type=int)
    parser.add_argument('--group-id', type=str)

    args = parser.parse_args()

    if args.token:
        global TOKEN
        TOKEN = args.token
    if args.to:
        global NOTIFY_CHAT_ID
        NOTIFY_CHAT_ID = args.to
    if args.group_id:
        global WATCH_ID
        WATCH_ID = args.group_id
    if args.interval:
        global INTERVAL
        INTERVAL = args.interval

    print('telegram admin helper')
    
    get_updates(BASE_URL + 'getUpdates')


if __name__ == '__main__':
    main()

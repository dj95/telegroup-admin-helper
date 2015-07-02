#!/bin/env python3
#
# telegram admin helper
#
# © 2015 Daniel Jankowski
# Licensed under the LGPLv3

import urllib.request
import json
import time

INTERVAL=5 # interval before getting new updates

NOTIFY_CHAT_ID='' # chat id of group or user, who should receive the notification
WATCH_ID='' # chat id of group chat to watch
BANNED_NICK_NAMES=[''] # banned nicknames

TOKEN='' # access token for your bot
BASE_URL='https://api.telegram.org/bot' + TOKEN + '/' # base url for bots (DON'T CHANGE!)

# TODO: test for update_id (so notifications will not be send twice)
def get_updates(url):
    rqst=urllib.request.urlopen(url)
    data=json.loads(rqst.read().decode('utf-8'))
    for i in range(len(data['result'])):
        msg=data['result'][i]
        if (msg['message']['chat']['id'] == WATCH_ID):
            if (msg['message']['chat']['from']['username'] in BANNED_NICK_NAMES):
                send_notification('WARNING: ' + msg['message'][' chaat']['from']['username'] + 'rejoined Group' + msg['message']['chat']['title'])


def send_notification(notification):
    msg='chat_id=' + NOTIFY_CHAT_ID + '&text=' + notification
    rqst=urllib.request.urlopen(BASE_URL + 'sendMessage', msg.encode('utf-8'))
    data=json.loads(rqst.read().decode('utf-8'))


def main():
    print('telegram admin helper')
    while True:
        get_updates(BASE_URL + 'getUpdates')
        time.sleep(INTERVAL)


if __name__ == '__main__':
    main()

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
import os
import re

INTERVAL = 5 # interval before getting new updates

NOTIFY_CHAT_ID = '' # chat id of group or user, who should receive the notification
WATCH_ID = 0 # chat id of group chat to watch
BANNED_NICK_NAMES = [''] # banned nicknames

TOKEN = '' # access token for your bot
BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/' # base url for bots (DON'T CHANGE!)

SAVE_FILE='/var/lib/telegroup-admin-helper/update_id.data'
CONFIG_FILE='/etc/telegroup-admin-helper'

def get_updates(url):
    old_update_id = 0
    global BANNED_NICK_NAMES
    while True:
        rqst = urllib.request.urlopen(url)
        data = json.loads(rqst.read().decode('utf-8'))
        for i in range(len(data['result'])):
            msg = data['result'][i]
            if msg['message']['chat']['id'] == WATCH_ID:
                if 'new_chat_participant' in msg['message']:
                    if msg['message']['new_chat_participant']['username'] in BANNED_NICK_NAMES:
                        if check_update_id(msg['update_id']):
                            send_notification('WARNING: ' + msg['message']['new_chat_participant']['username'] + ' rejoined Group ' + msg['message']['chat']['title'])
                            old_update_id = msg['update_id']
        # reparse config if new nicks are banned
        notify_id, watch_id, token, banned_nicks, interval = parse_config()
        if BANNED_NICK_NAMES is not banned_nicks and banned_nicks is not ['']:
            BANNED_NICK_NAMES = banned_nicks
        time.sleep(INTERVAL)


def check_update_id(new_id):
    new_id = str(new_id)
    if os.path.isfile(SAVE_FILE):
        f = open(SAVE_FILE, 'r')
        line = f.readline()
        f.close()
        old_id = line
    else:
        old_id = '0'
    if new_id > old_id:
        f = open(SAVE_FILE, 'w+')
        f.write(new_id)
        f.close()
        return True
    else:
        return False


def send_notification(notification):
    msg = 'chat_id=' + NOTIFY_CHAT_ID + '&text=' + notification
    rqst = urllib.request.urlopen(BASE_URL + 'sendMessage', msg.encode('utf-8'))
    data = json.loads(rqst.read().decode('utf-8'))


def parse_config():
    notify_id, watch_id, token, banned_nicks, interval = '', '', '', [''], ''
    if os.path.isfile(CONFIG_FILE):
        f = open(CONFIG_FILE, 'r')
        line = f.readlines()
        for i in range(len(line)):
            if not line[i].startswith('#') and not line[i].startswith('\n'):
                if line[i].startswith('NOTIFY_CHAT_ID'):
                    notify_id = re.sub('\n', '', re.sub('NOTIFY_CHAT_ID=','', line[i]))
                if line[i].startswith('WATCH_ID'):
                    watch_id = re.sub('\n', '', re.sub('WATCH_ID=','', line[i]))
                if line[i].startswith('TOKEN'):
                    token = re.sub('\n', '', re.sub('TOKEN=','', line[i]))
                if line[i].startswith('BANNED_NICK_NAMES'):
                    banned_nicks = re.sub('\n', '', re.sub('BANNED_NICK_NAMES=','', line[i]))
                    banned_nicks = banned_nicks.split(',')
                if line[i].startswith('INTERVAL'):
                    interval = re.sub('\n', '', re.sub('INTERVAL=','', line[i]))
        return notify_id, watch_id, token, banned_nicks, interval


def main():
    # parse config
    global NOTIFY_CHAT_ID
    global WATCH_ID
    global TOKEN
    global BANNED_NICK_NAMES
    global INTERVAL
    notify_id, watch_id, token, banned_nicks, interval = parse_config()
    if notify_id is not '' and watch_id is not '' and token is not '' and interval is not '':
        NOTIFY_CHAT_ID = notify_id
        WATCH_ID = int(watch_id)
        TOKEN = token
        BANNED_NICK_NAMES = banned_nicks
        INTERVAL = float(interval)
    else:
        print('ERROR: Please set your config correctly!')

    # arg parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('--to', type=str)
    parser.add_argument('--token', type=str)
    parser.add_argument('--interval', type=int)
    parser.add_argument('--group-id', type=str)

    args = parser.parse_args()

    if args.token:
        TOKEN = args.token
    if args.to:
        NOTIFY_CHAT_ID = args.to
    if args.group_id:
        WATCH_ID = args.group_id
    if args.interval:
        INTERVAL = args.interval

    # check if data path exists
    if not os.path.isdir('/var/lib/telegroup-admin-helper'):
        os.mkdir('/var/lib/telegroup-admin-helper')

    print('telegram admin helper')
    global BASE_URL
    BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/' # base url for bots (DON'T CHANGE!)
    get_updates(BASE_URL + 'getUpdates')


if __name__ == '__main__':
    main()

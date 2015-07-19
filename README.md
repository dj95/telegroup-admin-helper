telegroup-admin-helper
=====================

Simple Python script for use with official Telegram bots.

[![endorse](https://api.coderwall.com/dj95/endorsecount.png)](https://coderwall.com/dj95)


Features
--------

- checks in intervalls if banned usernames rejoined the group
- if banned user rejoins the group, a notification will be sent
- config file


Installation
------------

- Copy telegroup-admin-helper to /etc/ with `sudo cp telegroup-admin-helper /etc/`
- Edit the config properly, otherwise the bot doesn't work!
- Run the program with `sudo ./telegram-admin-helper.py &` to run in background or
    `sudo ./telegram-admin-helper.py` to run in foreground


**Hint:** To get the id of you and your group use https://api.telegram.org/botTOKEN/getUpdates and replace TOKEN with your bot-token.

**Hint:** If the bot doesnt recognize messages and user-joins, please disable privacy mode. If privacy-mode is activated, it won't recognize messages and actions, that aren't adressed directly to the bot,


Input parameters
----------------

```
usage: telegram-admin-helper.py [-h] [--to TO] [--token TOKEN]
                                [--interval INTERVAL] [--group-id GROUP_ID]

optional arguments:
  -h, --help           show this help message and exit
  --to TO              ID, which should get the notification
  --token TOKEN        token of your bot
  --interval INTERVAL  interval between two updates
  --group-id GROUP_ID  ID of group, which should be watched
```


TODO
----

- autokick (if possible)


License
-------

(c) 2015 Daniel Jankowski
Licensed under the GNU Lesser General Public License 3 (LGPLv3). See [LICENSE](./LICENSE) for details.

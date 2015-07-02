telegroup-admin-helper
=====================

Simple Python script for use with official Telegram bots.


Features
--------

- checks in intervalls if banned usernames rejoined the group
- if banned user rejoins the group, a notification will be sent


Input parameters
----------------

```
usage: telegram-admin-helper.py [-h] [--to TO] [--token TOKEN]
                                [--interval INTERVAL] [--group-id GROUP_ID]

optional arguments:
  -h, --help           show this help message and exit
  --to TO
  --token TOKEN
  --interval INTERVAL
  --group-id GROUP_ID

```


TODO
----

- config file
- autokick (if possible)


License
-------

(c) 2015 Daniel Jankowski
Licensed under the GNU Lesser General Public License 3 (LGPLv3). See [LICENSE](./LICENSE) for details.

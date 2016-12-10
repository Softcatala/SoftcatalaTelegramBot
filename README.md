# Robot de Softcatalà

* **SoftcatalaBot** is a Telegram inline bot based on [@createeventbot](https://telegram.me/createeventbot).
* This bot is private, only users with permissions can create content :closed_lock_with_key:
* Idea: Organization administrators create content with this Telegram bot, and share it in a Telegram channel.
* Softcatalà is a non-profit organization: [**Softcatalà**](https://www.softcatala.org/) 

Descripció
----------

> El robot està pensat perquè només alguns administradors de Softcatalà puguin crear contingut, aquest és el motiu pel qual hi ha una part del robot que és privada.

> El robot publica al [canal de Softcatalà](https://telegram.me/CanalSoftcatala).

General usage
-------------

Usage: @celp_bot [content name]

Installation
------------

* First, you need Python 3 (pre-installed on Ubuntu) and package manager:
```
$sudo apt-get install python-pip3
```

Copy source files to your local machine or server.

Then, you need to install requirements. Go to the directory where requirements.txt are, and run:
```
$sudo pip3 install -r requirements.txt
```

Add your [Telegram token](https://github.com/Softcatala/SoftcatalaBot/blob/master/bot.py#L31)

Add your [allowed users id](https://github.com/Softcatala/SoftcatalaBot/blob/master/modules/commands.py#L181). <br/>You can know it with some bots like [@MyIDbot](http://telegram.me/myidbot).

And finally launch the bot with (in the directory where bot.py are):
```
$python3 bot.py
```

Credits
-------

* [Create-event-bot](https://github.com/lukaville/create-event-bot) by Nickolay Chameev

* Python packages:
  * [Parsedatetime](https://github.com/bear/parsedatetime) by Mike Taylor
  * [Python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
  * [Requests](https://github.com/kennethreitz/requests) by Kenneth Reitz
  * [TinyDB](https://github.com/msiemens/tinydb/) by Markus Siemens
  * [Validators](https://github.com/kvesteri/validators) by Konsta Vesterinen

* To generate add.html page:
  * [Base64.js](https://github.com/dankogai/js-base64) by Dan Kogai
  * [jQuery](https://jquery.com/)
  * [OuiCal](https://github.com/carlsednaoui/add-to-calendar-buttons) by Carl Sednaoui
  * [Twemoji](https://github.com/twitter/twemoji) by Twitter

* Bot images:
  * [Calendar](https://www.flickr.com/photos/dafnecholet/5374200948/in/photolist-9bUbH3-3xU18-9Tjoap-9Tjo7V-3qMfSb-rUyG8-6hEsk-3qMfY7-76v1pT-5SLjF-5vZnPr-bR4TB-2aNjrB-5jLKHc-7AC132-8QQ8K3-5U7uqn-9akFr6-9gZGC3-5r3sad-5r2wbo-5r2wGm-5r3nKN-5r3uYS-5r3uvA-sY9ob-aYAHs-cT9Bh-fgYtmY-9dQRes-5RHQEm-zBgjg-vj3yV-ymHeT-g8K8bv-7baY6F-aGRbBg-6hByqe-5r3rBf-5qY2DH-5r3tBY-5qY8AB-qm28Qn-5qY9ut-5qY3yF-5qYb28-rL7o8-5r2x8f-5qY85t-5NEAjs) by Dafne Cholet [(CC BY 2.0)](https://creativecommons.org/licenses/by/2.0/)
  * [Jornada de traducció de Softcatalà - Octubre 2011](https://m.flickr.com/#/photos/toniher/6268729872/in/search_QM_q_IS_Softcatal%C3%A0) by Toni Hermoso [(CC BY-SA 2.0)](https://creativecommons.org/licenses/by-sa/2.0/)
  * [keyboard](https://www.flickr.com/photos/jmettraux/5220192413/in/photolist-8XhRkt-5Wtibx-rmDdQY-bGGgo-a3zVtP-37eaR2-7qaBDG-9gN6ie-9BVHwp-qjWP6s-37iJVd-37eoTa-c28AgE-cwLmpd-6xVWmH-8RTE2g-sgf2sQ-rmDfcL-tfS3xJ-tfTcFJ-xNNHo6-bvVDie-atqZco-wR9Mt9-o4EsFw-bJVsqi-5ioxWq-569niC-6dYoeL-9HSWiz-bFxRCV-5tWxwf-5tWxV3-5ruKUB-5C1JTQ-7FpHQ2-7x7o1q-f9k3W7-6dUeti-jGGjMu-d8atD7-5tSaJe-sAsgP5-e76Sjz-9BVHmk-8jqLdc-6sHJFL-g9FyfG-6aGnjW-DWtde) by jmettraux [(CC BY 2.0)](https://creativecommons.org/licenses/by/2.0/)

* Logo:
  * :copyright: [Softcatalà logo]() need permissions?

Contact
-------

* lakonfrariadelavila *at* gmail *dot* com

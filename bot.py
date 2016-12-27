#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Create calendar events inline bot

import logging
import os

from telegram.ext import Updater
from requests import get
import requests
import json

from threading import Thread
import time
import schedule

from modules.commands import CommandsModule
from modules.inline import InlineModule
from modules.langpack import LangpackModule

from config import params, paths, chats

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def error(bot, update, err):
    logger.warn('Update "%s" caused error "%s"' % (update, err))


def load_modules(dispatcher, modules):
    for module in modules:
        for handler in module.get_handlers():
            dispatcher.add_handler(handler)

def main():
    updater = Updater(params['token'])

    dp = updater.dispatcher

    load_modules(dp, [LangpackModule(), CommandsModule(), InlineModule()])

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

def job():
     testfiles= 0
     #TEST ANDROID FILE_ID
     f= open(paths['file_ids']+"android_file_id.txt","r")
     fandroid= f.read(32)
     f.close()
     r = requests.get('https://api.telegram.org/bot' + params['token'] + '/getFile?file_id=' + fandroid)
     output= r.json()
     if output['ok']:
           testandroid= ''
     else:
           testfiles+= 1
           testandroid= '*Android*%20'
     #TEST IOS FILE_ID
     f= open(paths['file_ids']+"ios_file_id.txt","r")
     fios= f.read(32)
     f.close()
     r = requests.get('https://api.telegram.org/bot' + params['token'] + '/getFile?file_id=' + fios)
     output= r.json()
     if output['ok']:
           testios= ''
     else:
           testfiles+= 1
           testios= '*iOS*%20'
     #TEST TELEGRAM DESKTOP FILE_ID
     f= open(paths['file_ids']+"tdesktop_file_id.txt","r")
     ftdesktop= f.read(32)
     f.close()
     r = requests.get('https://api.telegram.org/bot' + params['token'] + '/getFile?file_id=' + ftdesktop)
     output= r.json()
     if output['ok']:
           testtdesktop= ''
     else:
           testfiles+= 1
           testtdesktop= '*Telegram%20Desktop*%20'
     if testfiles == 0:
         r = requests.get('https://api.telegram.org/bot' + params['token'] + '/sendMessage?chat_id=' + chats['group'] + '&text=Els%20*file_id*%20dels%20tres%20fitxers%20s%C3%B3n%20correctes.%20No%20hi%20ha%20cap%20error.&parse_mode=Markdown')
         return r

     elif testfiles == 1:
         r = requests.get('https://api.telegram.org/bot' + params['token'] + '/sendMessage?chat_id=' + chats['group'] + '&text=S%27ha%20trobat%20un%20error%20al%20*file_id*%20del%20paquet%20de%20llengua%20per%20a%20' + testandroid + testios + testtdesktop + '&parse_mode=Markdown')
         return r
     elif testfiles > 1:
         r = requests.get('https://api.telegram.org/bot' + params['token'] + '/sendMessage?chat_id=' + chats['group'] + '&text=S%27han%20trobat%20' + str(testfiles) + '%20errors%20als%20*file_id*%20dels%20paquet%20de%20llengua%3A%20' + testandroid + testios + testtdesktop + '&parse_mode=Markdown')
         return r

#schedule.every(1).minutes.do(job)
schedule.every().day.at("17:14").do(job)

def spawn():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    Thread(target=spawn).start()
    main()

# -*- coding: utf-8 -*-

import time
import csv

from requests import get
import requests
import json

from datetime import datetime

from parsedatetime import parsedatetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardHide
from telegram.ext import CommandHandler, MessageHandler, Filters, InlineQueryHandler, CallbackQueryHandler, Updater, Job

from store import TinyDBStore
from modules.inline import InlineModule

from config import params, allowed_users, paths, chats, inline_status


class LangpackModule(object):
    def __init__(self):
        self.handlers = [
            CommandHandler('start', self.download_command, pass_args=True),
            CommandHandler('baixa', self.download_command, pass_args=True),
            CommandHandler('android', self.android_command),
            CommandHandler('ios', self.ios_command),
            CommandHandler('tdesktop', self.tdesktop_command),
            CommandHandler('stats', self.stats_command),
            CommandHandler('getfiles', self.getfiles_command),
            CommandHandler('testfiles', self.testfiles_command),
            CallbackQueryHandler(self.platform_handler)
            #MessageHandler([Filters.text], self.message)
        ]
        self.store = TinyDBStore()
        self.inline = InlineModule()

    def testfiles_command(self, bot, update):
        user_id = update.message.from_user.id
        if str(user_id) in allowed_users.values():
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
                   testandroid= '    \U0001F6AB *Android*\n'
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
                   testios= '    \U0001F6AB *iOS*\n'
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
                   testtdesktop= '    \U0001F6AB *Telegram Desktop*\n'
             if testfiles == 0:
                 bot.sendMessage(update.message.from_user.id,
                      parse_mode='Markdown',
                      text= "Els *file_id* dels tres fitxers són correctes.\nHi ha " + str(testfiles) + " errors.")
             elif testfiles > 0:
                 bot.sendMessage(update.message.from_user.id,
                      parse_mode='Markdown',
                      text= "Errors als *file_id* dels paquets de llengua: " +str(testfiles) + "\n  Fallen els paquets:\n" + testandroid + testios + testtdesktop)

    def callback_test(bot, job):
        #user_id = update.message.from_user.id
        #if str(user_id) in allowed_users.values():
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
                   testandroid= '    \U0001F6AB *Android*\n'
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
                   testios= '    \U0001F6AB *iOS*\n'
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
                   testtdesktop= '    \U0001F6AB *Telegram Desktop*\n'
             if testfiles == 0:
                 bot.sendMessage(chats['group'],
                      parse_mode='Markdown',
                      text= "Els *file_id* dels tres fitxers són correctes.\nHi ha " + str(testfiles) + " errors.")
             elif testfiles > 0:
                 bot.sendMessage(chats['group'],
                      parse_mode='Markdown',
                      text= "Errors als *file_id* dels paquets de llengua: " +str(testfiles) + "\n  Fallen els paquets:\n" + testandroid + testios + testtdesktop)

    updater = Updater(params['token'])
    j = updater.job_queue
    job_minute = Job(callback_test, 43200.0)
    j.put(job_minute, next_t=43200.0)
    j.start()

    def platform_handler(self, bot, update):
        f= open(paths['versions']+"android_version.txt","r")
        and_version= f.read(10)
        f.close()
        f= open(paths['versions']+"ios_version.txt","r")
        ios_version= f.read(10)
        f.close()
        f= open(paths['versions']+"tdesktop_version.txt","r")
        tdesk_version= f.read(10)
        f.close()
        tandroid= "Heu triat el paquet de llengua per a *Telegram Android*.\n\nUs enviem la versió " + str(and_version) + " del paquet. Podeu demanar-ne la versió més actual sempre que ho desitgeu.\n\n*Instruccions d'instal·lació*:\n1r. *Baixeu el fitxer* «strings.xml» enviat després d'aquest missatge prement la icona de la fletxa cap avall.\n2n. Feu clic al símbol ⋮ per a obrir el *menú d'opcions*.\n3r. Trieu «Apply localization file», «Aplicar traducción» o «Aplica el paquet de llengua», segons el cas.\n4t. Trieu l'opció «Català».\n\nSi voleu que us avisem quan hi hagi una versió nova del paquet de llengua, o notícies de Softcatalà, uniu-vos al [Canal de Softcatalà](https://telegram.me/CanalSoftcatala)."
        tios= "Heu triat el paquet de llengua per a *Telegram iOS*.\n\nUs enviem la versió " + str(ios_version) + " del paquet. Podeu demanar-ne la versió més actual sempre que ho desitgeu.\n\n*Instruccions d'instal·lació*:\n1r. *Baixeu el fitxer* «Localizable-ios.strings» enviat després d'aquest missatge prement la icona de la fletxa cap avall.\n2n. Premeu sobre el fitxer baixat i trieu «Apply localization file», «Aplicar traducción» o «Aplica el paquet de llengua», segons el cas.\n\nSi voleu que us avisem quan hi hagi una versió nova del paquet de llengua, o notícies de Softcatalà, uniu-vos al [Canal de Softcatalà](https://telegram.me/CanalSoftcatala)."
        ttdesktop= "Heu triat el paquet de llengua per a *Telegram Desktop*.\n\nUs enviem la versió " + str(tdesk_version) + " del paquet. Podeu demanar-ne la versió més actual sempre que ho desitgeu.\n\n*Intruccions d'instal·lació*:\n1r. *Baixeu el fitxer* «tdesktop.strings» enviat després d'aquest missatge i recordeu la carpeta on es troba, habitualment `./Baixades/Telegram Desktop` del vostre perfil d'usuari.\n2n. Aneu a la configuració del Telegram Desktop («Settings» o «Ajustes») i, *a l'aire, teclegeu* «loadlang».\n3r. Trieu el fitxer «tdesktop.strings» baixat al pas 1.\n4t. Confirmeu el reinici del Telegram Desktop.\n\n*Nota*: no esborreu de l'ordinador el fitxer que heu baixat.\n\nSi voleu que us avisem quan hi hagi una versió nova del paquet de llengua, o notícies de Softcatalà, uniu-vos al [Canal de Softcatalà](https://telegram.me/CanalSoftcatala)."
        f= open(paths['file_ids']+"android_file_id.txt","r")
        fandroid= f.read(32)
        f.close()
        f= open(paths['file_ids']+"ios_file_id.txt","r")
        fios= f.read(32)
        f.close()
        f= open(paths['file_ids']+"tdesktop_file_id.txt","r")
        ftdesktop= f.read(32)
        f.close()
	
        if update.callback_query:
        #SI LA FUNCIÓ LA TRIGA UN BOTÓ INTEGRAT (ÉS A DIR, SI EXISTEIX UN CALLBACK_QUERY).
            query = update.callback_query
            data = query.data	
            if data != 'Android' and data != 'iOS' and data != 'tdesktop':
                 print (query)
                 print (data)
                 if data.startswith( 'go_' ) or data.startswith( 'like_' ) or data.startswith( 'nolike_' ):
                     user = query.from_user.__dict__
                     (command, event_id) = tuple(data.split('_'))
                     event = self.store.get_event(event_id)
                     self.inline.callback_handler(bot, update)
        else:
        #SI LA FUNCIÓ LA TRIGA L'ORDRE «/start argument» (ÉS A DIR, SI NO EXISTEIX UN CALLBACK_QUERY).
            query = update.message
            data = query.text
            if data != 'Android' and data != 'iOS' and data != 'tdesktop':
                 if data.startswith( 'go_' ) or data.startswith( 'like_' ) or data.startswith( 'nolike_' ):
                     user = query.from_user.__dict__
                     (command, event_id) = tuple(data.split('_'))
                     event = self.store.get_event(event_id)
                     self.inline.callback_handler(bot, update)
        #ACÍ HI HAURA QUE VEURE LA FORMA DE TRAURE-LI EL «/start» AL message.text.		

        if data == 'Android':
              filepack= fandroid
              textpack= tandroid
        elif data == 'iOS':
              filepack= fios
              textpack= tios
        elif data == 'tdesktop':
              filepack= ftdesktop
              textpack= ttdesktop

        if data == 'Android' or data == 'iOS' or data == 'tdesktop':
               bot.sendMessage(chat_id=query.message.chat_id,
               #bot.editMessageText(chat_id=query.message.chat_id,
                                   #message_id=query.message.message_id,
		                   parse_mode='Markdown',
                                   disable_web_page_preview=True,
                                   text=textpack)

               bot.sendDocument(chat_id=query.message.chat_id,
                                #reply_to_message_id=query.message.message_id,
                                document=filepack)

               user_id = update.callback_query.from_user.id
               today= datetime.now()
               dayraw = today.day
               if int(dayraw) < 10:
                  day = '0' + str(dayraw)
               else:
                  day = str(dayraw)
               monthraw = today.month
               if int(monthraw) < 10:
                  month = '0' + str(monthraw)
               else:
                  month = str(monthraw)
               year = today.year
               today2= day + '/' + month + '/' + str(year)

               if data == 'Android':
                   stat= today2 + ';user#id' + str(user_id) + ';' + str(and_version) + ';' + data + ';bot;buttons'
               elif data == "iOS":
                   stat= today2 + ';user#id' + str(user_id) + ';' + str(ios_version) + ';' + data + ';bot;buttons'
               elif data == "tdesktop":
                   stat= today2 + ';user#id' + str(user_id) + ';' + str(tdesk_version) + ';' + data + ';bot;buttons'
               with open(paths['stats']+'stats.csv','a',newline='') as f:
                    writer=csv.writer(f)
                    writer.writerow([stat])

               callback_query_id=query.id
               bot.answerCallbackQuery(callback_query_id=query.id, text="S'ha enviat el paquet.")

    def getfiles_command(self, bot, update):
        user_id = update.message.from_user.id
        if str(user_id) in allowed_users.values():
            bot.sendMessage(update.message.chat_id,
                            parse_mode='Markdown',
                            text= "Us envio els fitxers desats al servidor (còpia de seguretat) per a cada plataforma. Veureu que hi ha la versió normal i la versió desada amb la data (els dos fitxers han de ser iguals)."
            )
            #SEND LOCAL ANDROID FILES
            f= open(paths['versions']+"android_version.txt","r")
            and_version= f.read(10)
            f.close()
            and_version2= str.replace(and_version, "/", "-")
            android_file= open(paths['local_packs']+'strings.xml', 'rb')
            bot.sendDocument(update.message.chat_id,
                             document=android_file)
            android_file_v= open(paths['local_packs']+'strings-' +and_version2+ '.xml', 'rb')
            bot.sendDocument(update.message.chat_id,
                             document=android_file_v)
            #SEND LOCAL IOS FILES
            f= open(paths['versions']+"ios_version.txt","r")
            ios_version= f.read(10)
            f.close()
            ios_version2= str.replace(ios_version, "/", "-")
            ios_file= open(paths['local_packs']+'Localizable-ios.strings', 'rb')
            bot.sendDocument(update.message.chat_id,
                             document=ios_file)
            ios_file_v= open(paths['local_packs']+'Localizable-ios-' +and_version2+ '.strings', 'rb')
            bot.sendDocument(update.message.chat_id,
                             document=ios_file_v)
            #SEND LOCAL TELEGRAM DESKTOP FILES
            f= open(paths['versions']+"tdesktop_version.txt","r")
            tdesk_version= f.read(10)
            f.close()
            tdesk_version2= str.replace(tdesk_version, "/", "-")
            tdesktop_file= open(paths['local_packs']+'tdesktop.strings', 'rb')
            bot.sendDocument(update.message.chat_id,
                             document=tdesktop_file)
            tdesktop_file_v= open(paths['local_packs']+'tdesktop-' +tdesk_version2+ '.strings', 'rb')
            bot.sendDocument(update.message.chat_id,
                             document=tdesktop_file_v) 

    def download_command(self, bot, update, args):
        user_id = update.message.from_user.id
        if str(user_id) in allowed_users.values():
            if len(args) == 0:
                keyboard = [[InlineKeyboardButton("Android", callback_data='Android'),
                         InlineKeyboardButton("iOS", callback_data='iOS'),
		         InlineKeyboardButton("TDesktop", callback_data='tdesktop')]]

                bot.sendMessage(update.message.chat_id,
                            parse_mode='Markdown',
                            text= "Hola, sóc el *Robot de Softcatalà*! La meva funció és proporcionar els paquets de llengua per a les diferents aplicacions del Telegram que els admeten.\nTrieu el sistema operatiu que esteu utilitzant per baixar el paquet de llengua adequat:",
                            reply_markup = InlineKeyboardMarkup(keyboard)
                )
            elif len(args) == 1 and args[0] == 'android-rebost':
                  user_id = update.message.from_user.id
                  if str(user_id) in allowed_users.values():
                      f= open(paths['versions']+"android_version.txt","r")
                      and_version= f.read(10)
                      f.close()
                      tandroid= "Heu triat el paquet de llengua per a *Telegram Android*.\n\nUs enviem la versió " + str(and_version) + " del paquet. Podeu demanar-ne la versió més actual sempre que ho desitgeu.\n\n*Instruccions d'instal·lació*:\n1r. *Baixeu el fitxer* «strings.xml» enviat després d'aquest missatge prement la icona de la fletxa cap avall.\n2n. Feu clic al símbol ⋮ per a obrir el *menú d'opcions*.\n3r. Trieu «Apply localization file», «Aplicar traducción» o «Aplica el paquet de llengua», segons el cas.\n4t. Trieu l'opció «Català».\n\nSi voleu que us avisem quan hi hagi una versió nova del paquet de llengua, o notícies de Softcatalà, uniu-vos al [Canal de Softcatalà](https://telegram.me/CanalSoftcatala)."
                      f= open(paths['file_ids']+"android_file_id.txt","r")
                      fandroid= f.read(32)
                      f.close()
                      bot.sendMessage(update.message.chat_id,
                                      parse_mode='Markdown',
                                      disable_web_page_preview=True,
                                      text= tandroid
                      )
                      bot.sendDocument(update.message.chat_id,
                                       document=fandroid)

                      user_id = update.message.from_user.id
                      today= datetime.now()
                      dayraw = today.day
                      if int(dayraw) < 10:
                          day = '0' + str(dayraw)
                      else:
                          day = str(dayraw)
                      monthraw = today.month
                      if int(monthraw) < 10:
                          month = '0' + str(monthraw)
                      else:
                          month = str(monthraw)
                      year = today.year
                      today2= day + '/' + month + '/' + str(year)

                      stat= today2 + ';user#id' + str(user_id) + ';' + str(and_version) + ';Android;web;rebost'
                      with open(paths['stats']+'stats.csv','a',newline='') as f:
                          writer=csv.writer(f)
                          writer.writerow([stat])
            elif len(args) == 1 and args[0] == 'ios-rebost':
                  user_id = update.message.from_user.id
                  if str(user_id) in allowed_users.values():
                      f= open(paths['versions']+"ios_version.txt","r")
                      ios_version= f.read(10)
                      f.close()
                      tios= "Heu triat el paquet de llengua per a *Telegram iOS*.\n\nUs enviem la versió " + str(ios_version) + " del paquet. Podeu demanar-ne la versió més actual sempre que ho desitgeu.\n\n*Instruccions d'instal·lació*:\n1r. *Baixeu el fitxer* «Localizable-ios.strings» enviat després d'aquest missatge prement la icona de la fletxa cap avall.\n2n. Premeu sobre el fitxer baixat i trieu «Apply localization file», «Aplicar traducción» o «Aplica el paquet de llengua», segons el cas.\n\nSi voleu que us avisem quan hi hagi una versió nova del paquet de llengua, o notícies de Softcatalà, uniu-vos al [Canal de Softcatalà](https://telegram.me/CanalSoftcatala)."
                      f= open(paths['file_ids']+"ios_file_id.txt","r")
                      fios= f.read(32)
                      f.close()
                      bot.sendMessage(update.message.chat_id,
                                      parse_mode='Markdown',
                                      disable_web_page_preview=True,
                                      text= tios
                      )
                      bot.sendDocument(update.message.chat_id,
                                       document=fios)

                      user_id = update.message.from_user.id
                      today= datetime.now()
                      dayraw = today.day
                      if int(dayraw) < 10:
                          day = '0' + str(dayraw)
                      else:
                          day = str(dayraw)
                      monthraw = today.month
                      if int(monthraw) < 10:
                          month = '0' + str(monthraw)
                      else:
                          month = str(monthraw)
                      year = today.year
                      today2= day + '/' + month + '/' + str(year)

                      stat= today2 + ';user#id' + str(user_id) + ';' + str(ios_version) + ';iOS;web;rebost'
                      with open(paths['stats']+'stats.csv','a',newline='') as f:
                          writer=csv.writer(f)
                          writer.writerow([stat])
            elif len(args) == 1 and args[0] == 'tdesktop-rebost':
                  user_id = update.message.from_user.id
                  if str(user_id) in allowed_users.values():
                      f= open(paths['versions']+"tdesktop_version.txt","r")
                      tdesk_version= f.read(10)
                      f.close()
                      ttdesktop= "Heu triat el paquet de llengua per a *Telegram Desktop*.\n\nUs enviem la versió " + str(tdesk_version) + " del paquet. Podeu demanar-ne la versió més actual sempre que ho desitgeu.\n\n*Intruccions d'instal·lació*:\n1r. *Baixeu el fitxer* «tdesktop.strings» enviat després d'aquest missatge i recordeu la carpeta on es troba, habitualment `./Baixades/Telegram Desktop` del vostre perfil d'usuari.\n2n. Aneu a la configuració del Telegram Desktop («Settings» o «Ajustes») i, *a l'aire, teclegeu* «loadlang».\n3r. Trieu el fitxer «tdesktop.strings» baixat al pas 1.\n4t. Confirmeu el reinici del Telegram Desktop.\n\n*Nota*: no esborreu de l'ordinador el fitxer que heu baixat.\n\nSi voleu que us avisem quan hi hagi una versió nova del paquet de llengua, o notícies de Softcatalà, uniu-vos al [Canal de Softcatalà](https://telegram.me/CanalSoftcatala)."
                      f= open(paths['file_ids']+"tdesktop_file_id.txt","r")
                      ftdesktop= f.read(32)
                      f.close()
                      bot.sendMessage(update.message.chat_id,
                                      parse_mode='Markdown',
                                      disable_web_page_preview=True,
                                      text= ttdesktop
                      )
                      bot.sendDocument(update.message.chat_id,
                                       document=ftdesktop)

                      user_id = update.message.from_user.id
                      today= datetime.now()
                      dayraw = today.day
                      if int(dayraw) < 10:
                          day = '0' + str(dayraw)
                      else:
                          day = str(dayraw)
                      monthraw = today.month
                      if int(monthraw) < 10:
                          month = '0' + str(monthraw)
                      else:
                          month = str(monthraw)
                      year = today.year
                      today2= day + '/' + month + '/' + str(year)

                      stat= today2 + ';user#id' + str(user_id) + ';' + str(tdesk_version) + ';tdesktop;web;rebost'
                      with open(paths['stats']+'stats.csv','a',newline='') as f:
                          writer=csv.writer(f)
                          writer.writerow([stat])
            elif len(args) == 1 and args[0] == 'android-channel':
                  user_id = update.message.from_user.id
                  if str(user_id) in allowed_users.values():
                      f= open(paths['versions']+"android_version.txt","r")
                      and_version= f.read(10)
                      f.close()
                      tandroid= "Heu triat el paquet de llengua per a *Telegram Android*.\n\nUs enviem la versió " + str(and_version) + " del paquet. Podeu demanar-ne la versió més actual sempre que ho desitgeu.\n\n*Instruccions d'instal·lació*:\n1r. *Baixeu el fitxer* «strings.xml» enviat després d'aquest missatge prement la icona de la fletxa cap avall.\n2n. Feu clic al símbol ⋮ per a obrir el *menú d'opcions*.\n3r. Trieu «Apply localization file», «Aplicar traducción» o «Aplica el paquet de llengua», segons el cas.\n4t. Trieu l'opció «Català».\n\nSi voleu que us avisem quan hi hagi una versió nova del paquet de llengua, o notícies de Softcatalà, uniu-vos al [Canal de Softcatalà](https://telegram.me/CanalSoftcatala)."
                      f= open(paths['file_ids']+"android_file_id.txt","r")
                      fandroid= f.read(32)
                      f.close()
                      bot.sendMessage(update.message.chat_id,
                                      parse_mode='Markdown',
                                      disable_web_page_preview=True,
                                      text= tandroid
                      )
                      bot.sendDocument(update.message.chat_id,
                                       document=fandroid)

                      user_id = update.message.from_user.id
                      today= datetime.now()
                      dayraw = today.day
                      if int(dayraw) < 10:
                          day = '0' + str(dayraw)
                      else:
                          day = str(dayraw)
                      monthraw = today.month
                      if int(monthraw) < 10:
                          month = '0' + str(monthraw)
                      else:
                          month = str(monthraw)
                      year = today.year
                      today2= day + '/' + month + '/' + str(year)

                      stat= today2 + ';user#id' + str(user_id) + ';' + str(and_version) + ';Android;channel;buttons'
                      with open(paths['stats']+'stats.csv','a',newline='') as f:
                          writer=csv.writer(f)
                          writer.writerow([stat])
            elif len(args) == 1 and args[0] == 'ios-channel':
                  user_id = update.message.from_user.id
                  if str(user_id) in allowed_users.values():
                      f= open(paths['versions']+"ios_version.txt","r")
                      ios_version= f.read(10)
                      f.close()
                      tios= "Heu triat el paquet de llengua per a *Telegram iOS*.\n\nUs enviem la versió " + str(ios_version) + " del paquet. Podeu demanar-ne la versió més actual sempre que ho desitgeu.\n\n*Instruccions d'instal·lació*:\n1r. *Baixeu el fitxer* «Localizable-ios.strings» enviat després d'aquest missatge prement la icona de la fletxa cap avall.\n2n. Premeu sobre el fitxer baixat i trieu «Apply localization file», «Aplicar traducción» o «Aplica el paquet de llengua», segons el cas.\n\nSi voleu que us avisem quan hi hagi una versió nova del paquet de llengua, o notícies de Softcatalà, uniu-vos al [Canal de Softcatalà](https://telegram.me/CanalSoftcatala)."
                      f= open(paths['file_ids']+"ios_file_id.txt","r")
                      fios= f.read(32)
                      f.close()
                      bot.sendMessage(update.message.chat_id,
                                      parse_mode='Markdown',
                                      disable_web_page_preview=True,
                                      text= tios
                      )
                      bot.sendDocument(update.message.chat_id,
                                       document=fios)

                      user_id = update.message.from_user.id
                      today= datetime.now()
                      dayraw = today.day
                      if int(dayraw) < 10:
                          day = '0' + str(dayraw)
                      else:
                          day = str(dayraw)
                      monthraw = today.month
                      if int(monthraw) < 10:
                          month = '0' + str(monthraw)
                      else:
                          month = str(monthraw)
                      year = today.year
                      today2= day + '/' + month + '/' + str(year)

                      stat= today2 + ';user#id' + str(user_id) + ';' + str(ios_version) + ';iOS;channel;buttons'
                      with open(paths['stats']+'stats.csv','a',newline='') as f:
                          writer=csv.writer(f)
                          writer.writerow([stat])
            elif len(args) == 1 and args[0] == 'tdesktop-channel':
                  user_id = update.message.from_user.id
                  if str(user_id) in allowed_users.values():
                      f= open(paths['versions']+"tdesktop_version.txt","r")
                      tdesk_version= f.read(10)
                      f.close()
                      ttdesktop= "Heu triat el paquet de llengua per a *Telegram Desktop*.\n\nUs enviem la versió " + str(tdesk_version) + " del paquet. Podeu demanar-ne la versió més actual sempre que ho desitgeu.\n\n*Intruccions d'instal·lació*:\n1r. *Baixeu el fitxer* «tdesktop.strings» enviat després d'aquest missatge i recordeu la carpeta on es troba, habitualment `./Baixades/Telegram Desktop` del vostre perfil d'usuari.\n2n. Aneu a la configuració del Telegram Desktop («Settings» o «Ajustes») i, *a l'aire, teclegeu* «loadlang».\n3r. Trieu el fitxer «tdesktop.strings» baixat al pas 1.\n4t. Confirmeu el reinici del Telegram Desktop.\n\n*Nota*: no esborreu de l'ordinador el fitxer que heu baixat.\n\nSi voleu que us avisem quan hi hagi una versió nova del paquet de llengua, o notícies de Softcatalà, uniu-vos al [Canal de Softcatalà](https://telegram.me/CanalSoftcatala)."
                      f= open(paths['file_ids']+"tdesktop_file_id.txt","r")
                      ftdesktop= f.read(32)
                      f.close()
                      bot.sendMessage(update.message.chat_id,
                                      parse_mode='Markdown',
                                      disable_web_page_preview=True,
                                      text= ttdesktop
                      )
                      bot.sendDocument(update.message.chat_id,
                                       document=ftdesktop)

                      user_id = update.message.from_user.id
                      today= datetime.now()
                      dayraw = today.day
                      if int(dayraw) < 10:
                          day = '0' + str(dayraw)
                      else:
                          day = str(dayraw)
                      monthraw = today.month
                      if int(monthraw) < 10:
                          month = '0' + str(monthraw)
                      else:
                          month = str(monthraw)
                      year = today.year
                      today2= day + '/' + month + '/' + str(year)

                      stat= today2 + ';user#id' + str(user_id) + ';' + str(tdesk_version) + ';tdesktop;channel;buttons'
                      with open(paths['stats']+'stats.csv','a',newline='') as f:
                          writer=csv.writer(f)
                          writer.writerow([stat])
            #CHANGE INLINE STATUS
            elif len(args) == 1 and args[0] == 'change-inline-status':
                  user_id = update.message.from_user.id
                  if str(user_id) in allowed_users.values():
                    with open(paths['inline']+'inline_status.csv', 'rt') as f:
                      reader = csv.reader(f, delimiter=',')
                      for row in reader:
                        for field in row:
                          if field == str(user_id) + '_admin':
                            status = {str(user_id): 'normal'}
                            inline_status.update(status)
                            with open(paths['inline']+'inline_status.csv', 'w') as f:
                                 [f.write('{0}_{1}\n'.format(key, value)) for key, value in inline_status.items()]
                            bot.sendMessage(update.message.chat_id,
			           parse_mode='Markdown',
			           text= "Ara sou un usuari *normal* per a les consultes _inline_."
	                    )
                          elif field == str(user_id) + '_normal':
                            status = {str(user_id): 'admin'}
                            inline_status.update(status)
                            with open(paths['inline']+'inline_status.csv', 'w') as f:
                                 [f.write('{0}_{1}\n'.format(key, value)) for key, value in inline_status.items()]
                            bot.sendMessage(update.message.chat_id,
			           parse_mode='Markdown',
			           text= "Ara sou un usuari *administrador* per a les consultes _inline_."
	                    )
            else:
                bot.sendMessage(update.message.chat_id,
			    parse_mode='Markdown',
			    text= "Ho lamento, aquesta ordre no accepta paràmetres. Envieu només /start."
	        )
        else:
            f_name = update.message.from_user.first_name
            bot.sendMessage(update.message.chat_id,
                            parse_mode='Markdown',
                            text= str(f_name) + ", aquest bot no és operatiu. Si cerqueu el paquet de llengua en català per al Telegram, aneu a @softcatala.")

    def android_command(self, bot, update):
        user_id = update.message.from_user.id
        if str(user_id) in allowed_users.values():
            f= open(paths['versions']+"android_version.txt","r")
            and_version= f.read(10)
            f.close()
            tandroid= "Heu triat el paquet de llengua per a *Telegram Android*.\n\nUs enviem la versió " + str(and_version) + " del paquet. Podeu demanar-ne la versió més actual sempre que ho desitgeu.\n\n*Instruccions d'instal·lació*:\n1r. *Baixeu el fitxer* «strings.xml» enviat després d'aquest missatge prement la icona de la fletxa cap avall.\n2n. Feu clic al símbol ⋮ per a obrir el *menú d'opcions*.\n3r. Trieu «Apply localization file», «Aplicar traducción» o «Aplica el paquet de llengua», segons el cas.\n4t. Trieu l'opció «Català».\n\nSi voleu que us avisem quan hi hagi una versió nova del paquet de llengua, o notícies de Softcatalà, uniu-vos al [Canal de Softcatalà](https://telegram.me/CanalSoftcatala)."
            f= open(paths['file_ids']+"android_file_id.txt","r")
            fandroid= f.read(32)
            f.close()
            bot.sendMessage(update.message.chat_id,
                            parse_mode='Markdown',
                            disable_web_page_preview=True,
                            text= tandroid
            )
            bot.sendDocument(update.message.chat_id,
                             document=fandroid)

            user_id = update.message.from_user.id
            today= datetime.now()
            dayraw = today.day
            if int(dayraw) < 10:
                day = '0' + str(dayraw)
            else:
                day = str(dayraw)
            monthraw = today.month
            if int(monthraw) < 10:
                month = '0' + str(monthraw)
            else:
                month = str(monthraw)
            year = today.year
            today2= day + '/' + month + '/' + str(year)

            stat= today2 + ';user#id' + str(user_id) + ';' + str(and_version) + ';Android;bot;command'
            with open(paths['stats']+'stats.csv','a',newline='') as f:
                writer=csv.writer(f)
                writer.writerow([stat])

        else:
            f_name = update.message.from_user.first_name
            bot.sendMessage(update.message.chat_id,
                            parse_mode='Markdown',
                            text= str(f_name) + ", aquest bot no és operatiu. Si cerqueu el paquet de llengua en català per al Telegram, aneu a @softcatala.")

    def ios_command(self, bot, update):
        user_id = update.message.from_user.id
        if str(user_id) in allowed_users.values():
            f= open(paths['versions']+"ios_version.txt","r")
            ios_version= f.read(10)
            f.close()
            tios= "Heu triat el paquet de llengua per a *Telegram iOS*.\n\nUs enviem la versió " + str(ios_version) + " del paquet. Podeu demanar-ne la versió més actual sempre que ho desitgeu.\n\n*Instruccions d'instal·lació*:\n1r. *Baixeu el fitxer* «Localizable-ios.strings» enviat després d'aquest missatge prement la icona de la fletxa cap avall.\n2n. Premeu sobre el fitxer baixat i trieu «Apply localization file», «Aplicar traducción» o «Aplica el paquet de llengua», segons el cas.\n\nSi voleu que us avisem quan hi hagi una versió nova del paquet de llengua, o notícies de Softcatalà, uniu-vos al [Canal de Softcatalà](https://telegram.me/CanalSoftcatala)."
            f= open(paths['file_ids']+"ios_file_id.txt","r")
            fios= f.read(32)
            f.close()
            bot.sendMessage(update.message.chat_id,
                            parse_mode='Markdown',
                            disable_web_page_preview=True,
                            text= tios
            )
            bot.sendDocument(update.message.chat_id,
                             document=fios)

            user_id = update.message.from_user.id
            today= datetime.now()
            dayraw = today.day
            if int(dayraw) < 10:
                day = '0' + str(dayraw)
            else:
                day = str(dayraw)
            monthraw = today.month
            if int(monthraw) < 10:
                month = '0' + str(monthraw)
            else:
                month = str(monthraw)
            year = today.year
            today2= day + '/' + month + '/' + str(year)

            stat= today2 + ';user#id' + str(user_id) + ';' + str(ios_version) + ';iOS;bot;command'
            with open(paths['stats']+'stats.csv','a',newline='') as f:
                writer=csv.writer(f)
                writer.writerow([stat])

        else:
            f_name = update.message.from_user.first_name
            bot.sendMessage(update.message.chat_id,
                            parse_mode='Markdown',
                            text= str(f_name) + ", aquest bot no és operatiu. Si cerqueu el paquet de llengua en català per al Telegram, aneu a @softcatala.")

    def tdesktop_command(self, bot, update):
        user_id = update.message.from_user.id
        if str(user_id) in allowed_users.values():
            f= open(paths['versions']+"tdesktop_version.txt","r")
            tdesk_version= f.read(10)
            f.close()
            ttdesktop= "Heu triat el paquet de llengua per a *Telegram Desktop*.\n\nUs enviem la versió " + str(tdesk_version) + " del paquet. Podeu demanar-ne la versió més actual sempre que ho desitgeu.\n\n*Intruccions d'instal·lació*:\n1r. *Baixeu el fitxer* «tdesktop.strings» enviat després d'aquest missatge i recordeu la carpeta on es troba, habitualment `./Baixades/Telegram Desktop` del vostre perfil d'usuari.\n2n. Aneu a la configuració del Telegram Desktop («Settings» o «Ajustes») i, *a l'aire, teclegeu* «loadlang».\n3r. Trieu el fitxer «tdesktop.strings» baixat al pas 1.\n4t. Confirmeu el reinici del Telegram Desktop.\n\n*Nota*: no esborreu de l'ordinador el fitxer que heu baixat.\n\nSi voleu que us avisem quan hi hagi una versió nova del paquet de llengua, o notícies de Softcatalà, uniu-vos al [Canal de Softcatalà](https://telegram.me/CanalSoftcatala)."
            f= open(paths['file_ids']+"tdesktop_file_id.txt","r")
            ftdesktop= f.read(32)
            f.close()
            bot.sendMessage(update.message.chat_id,
                            parse_mode='Markdown',
                            disable_web_page_preview=True,
                            text= ttdesktop
            )
            bot.sendDocument(update.message.chat_id,
                             document=ftdesktop)

            user_id = update.message.from_user.id
            today= datetime.now()
            dayraw = today.day
            if int(dayraw) < 10:
                day = '0' + str(dayraw)
            else:
                day = str(dayraw)
            monthraw = today.month
            if int(monthraw) < 10:
                month = '0' + str(monthraw)
            else:
                month = str(monthraw)
            year = today.year
            today2= day + '/' + month + '/' + str(year)

            stat= today2 + ';user#id' + str(user_id) + ';' + str(tdesk_version) + ';tdesktop;bot;command'
            with open(paths['stats']+'stats.csv','a',newline='') as f:
                writer=csv.writer(f)
                writer.writerow([stat])

        else:
            f_name = update.message.from_user.first_name
            bot.sendMessage(update.message.chat_id,
                            parse_mode='Markdown',
                            text= str(f_name) + ", aquest bot no és operatiu. Si cerqueu el paquet de llengua en català per al Telegram, aneu a @softcatala.")

    def stats_command(self, bot, update):
        user_id = update.message.from_user.id
        if str(user_id) in allowed_users.values():
            downloads = open(paths['stats']+'stats.csv', 'r')
            total = len(downloads.readlines())
            downloads.close()
            f = open(paths['stats']+"stats.csv", "r")
            downand = 0
            for line in f:
                  if line.split(';')[3].rstrip() == "Android":
                           downand += 1
            f.close()
            downand1= downand * 100 / total
            downand2= round(downand1,2)
            downand3= str(downand2)
            downand4= downand3.replace('.',',')
            g = open(paths['stats']+"stats.csv", "r")
            downios = 0
            for line in g:
                  if line.split(';')[3].rstrip() == "iOS":
                           downios += 1
            g.close()
            downios1= downios * 100 / total
            downios2= round(downios1,2)
            downios3= str(downios2)
            downios4= downios3.replace('.',',')
            h = open(paths['stats']+"stats.csv", "r")
            downtdesk= 0
            for line in h:
                  if line.split(';')[3].rstrip() == "tdesktop":
                           downtdesk += 1
            h.close()
            downtdesk1= downtdesk * 100 / total
            downtdesk2= round(downtdesk1,2)
            downtdesk3= str(downtdesk2)
            downtdesk4= downtdesk3.replace('.',',')
            bot.sendMessage(update.message.chat_id,
                            parse_mode='Markdown',
                            disable_web_page_preview=True,
                            text= "\U0001F4C8 *Estadístiques del bot*\n\nTotal: *" + str(total) + "* baixades.\n\n\U0001F4E6 Android: *" +str(downand)+ "* baixades (_" + downand4+ "%_)\n\U0001F4E6 iOS: *" +str(downios)+ "* baixades (_" +downios4+ "%_)\n\U0001F4E6 Telegram Desktop: *" +str(downtdesk)+ "* baixades (_" +downtdesk4+ "%_)\n\nA continuació us envio el fitxer *stats.csv* amb la taula de dades."
            )
            stats_file= open(paths['stats']+'stats.csv', 'rb')
            bot.sendDocument(update.message.chat_id,
                             document=stats_file) 

        else:
            f_name = update.message.from_user.first_name
            bot.sendMessage(update.message.chat_id,
                            parse_mode='Markdown',
                            text= str(f_name) + ", aquest bot no és operatiu. Si cerqueu el paquet de llengua en català per al Telegram, aneu a @softcatala.")

    def get_handlers(self):
        return self.handlers

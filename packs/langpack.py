# -*- coding: utf-8 -*-

import time
import csv
from datetime import datetime

from parsedatetime import parsedatetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardHide
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler


class LangpackModule(object):
    def __init__(self):
        self.handlers2 = [
            CommandHandler('baixa', self.download_command),
            CallbackQueryHandler(self.platform_handler)
            #MessageHandler([Filters.text], self.message)
        ]

    def platform_handler(self, bot, update):
        query = update.callback_query
        platform_name= query.data
        if platform_name == 'Android':
              filepack= "packs/strings.xml"
              textpack= "Us enviem la versió 24/11/2016 del paquet de llengua. Podeu demanar la versió més actual del paquet sempre que ho desitgeu.\n\nInstruccions d'instal·lació:\n1r. Baixeu el fitxer «strings.xml» enviat després d'aquest missatge fent clic a la icona de fletxa avall.\n2n. Feu clic al símbol ⋮ per a obrir el menú d'opcions.\n3r. Trieu «Apply localization file», «Aplicar traducción» o «Aplica el paquet de llengua», segons el cas.\n4t. Trieu l'opció «Català».\n\nSi voleu que us avisem quan hi hagi una versió nova del paquet de llengua, o notícies de Softcatalà, uniu-vos al canal de Softcatalà (@CanalSoftcatala)."
        elif platform_name == 'iOS':
              filepack= "packs/Localizable-ios.strings"
              textpack= "Us enviem la versió 24/11/2016 del paquet de llengua. Podeu demanar la versió més actual del paquet sempre que ho desitgeu.\n\nInstruccions:\n1r. Baixeu el fitxer «Localizable-ios.strings» enviat.\n2n. Trieu «Apply localization file», «Aplicar traducción» o «Aplica el paquet de llengua», segons el cas.\nSi voleu que us avisem quan hi hagi una versió nova del paquet de llengua, o notícies de Softcatalà, uniu-vos al canal de Softcatalà (@CanalSoftcatala)."
        elif platform_name == 'tdesktop':
              filepack= "packs/tdesktop.strings"
              textpack= "Us enviem la versió 24/11/2016 del paquet de llengua. Podeu demanar la versió més actual del paquet sempre que ho desitgeu.\n\nIntruccions d'instal·lació:\n1r. Baixeu el fitxer «tdesktop.strings» enviat després d'aquest missatge i recordeu la carpeta on es troba, habitualment './Baixades/Telegram Desktop' del vostre perfil d'usuari.\n2n. Aneu a la configuració del Telegram Desktop («Settings» o «Ajustes», secció «General») i, a l'aire, escriviu «loadlang».\n3r. Trieu el fitxer «tdesktop.strings» baixat al pas 1.\n4t. Reinicieu el Telegram Desktop.\n\nNota: no esborreu de l'ordinador el fitxer que heu baixat.\n\nSi voleu que us avisem quan hi hagi una versió nova del paquet de llengua, o notícies de Softcatalà, uniu-vos al canal de Softcatalà (@CanalSoftcatala)."

        bot.editMessageText(chat_id=query.message.chat_id,
                            message_id=query.message.message_id,
		            parse_mode='Markdown',
                            text=textpack)

        bot.sendDocument(chat_id=query.message.chat_id,
                         reply_to_message_id=query.message.message_id,
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
        f= open("version.txt","r")
        version= f.read(10)
        f.close()

        stat= today2 + ';user#id' + str(user_id) + ';' + str(version) + ';' + platform_name
        with open('stats.csv','a',newline='') as f:
             writer=csv.writer(f)
             writer.writerow([stat])

    def download_command(self, bot, update):
        user_id = update.message.from_user.id
        # Replace USER_ID with your user_id number:
        if user_id == USER_ID:
            keyboard = [[InlineKeyboardButton("Android", callback_data='Android'),
                         InlineKeyboardButton("iOS", callback_data='iOS'),
                        #InlineKeyboardButton("Windows Phone", callback_data='WP'),
		         InlineKeyboardButton("TDesktop", callback_data='tdesktop')]]

            bot.sendMessage(update.message.chat_id,
                            parse_mode='Markdown',
                            text= "Hola, sóc el *Robot de Softcatalà*! La meua funció és proporcionar els paquets de llengua per a les diferents aplicacions del Telegram que els admeten.\nTrieu el sistema operatiu que esteu utilitzant per baixar el paquet de llengua adequat:",
                            reply_markup = InlineKeyboardMarkup(keyboard)
            )   

        else:
            f_name = update.message.from_user.first_name
            bot.sendMessage(update.message.chat_id,
                            parse_mode='Markdown',
                            text= str(f_name) + ", aquest bot no és operatiu. Si cerqueu el paquet de llengua en català per al Telegram, aneu a @softcatala.")

    def get_handlers2(self):
        return self.handlers2

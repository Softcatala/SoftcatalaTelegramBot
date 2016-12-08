# -*- coding: utf-8 -*-

import time
import csv
from datetime import datetime

from parsedatetime import parsedatetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardHide
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from validators import url, ValidationFailure

from store import TinyDBStore

FIELDS = [
    {
        'name': 'name',
        'message': '\u0031\u20E3 Envieu-me el *nom de la publicació*.\n\nPer a cancel·lar el procés envieu /cancel.',
        'required': True
    },
    {
        'name': 'type',
        'message': '\u0032\u20E3 Envieu-me el *tipus de publicació*.\n\nPer a cancel·lar el procés envieu /cancel.',
        'required': True
    },
    {
        'name': 'description',
        'message': '\u0033\u20E3 Envieu-me el *cos del missatge* per a la publicació.\n\nPer a cancel·lar el procés envieu /cancel.',
        'required': True
    },
    {
        'name': 'month',
        'message': '\u0034\u20E3 Ara m\'haureu d\'enviar la *data i hora* de l\'esdeveniment.\n\n\U0001F5D3 En primer lloc seleccioneu el *mes*:',
        'required': True
    },
    {
        'name': 'day',
        'message': '\U0001F5D3 En segon lloc, haureu de seleccionar el *dia*:',
        'required': True
    },
    {
        'name': 'year',
        'message': '\U0001F5D3 Seleccioneu l\'*any*:',
        'required': True
    },
    {
        'name': 'hour',
        'message': '\U0001F570 Seleccioneu l\'*hora*:',
        'required': True
    },
    {
        'name': 'minute',
        'message': '\U0001F570 I per acabar, seleccioneu el *minut* d\'entre els quatre quarts o escriviu qualsevol nombre entre 0 i 59:',
        'required': True
    },
    {
        'name': 'date',
        'message': 'Comproveu que la data és correcta (seguint l\'ordre *mes/dia/any hora:minut*) i si és així premeu el botó per a desar-la.\n\nPer a cancel·lar el procés envieu /cancel.',
        'required': True
    },
    {
        'name': 'place',
        'message': '\u0035\u20E3 Envieu-me el *lloc de l\'esdeveniment*.\n\nPodeu enviar /skip per a deixar el camp en blanc o /cancel per a cancel·lar la creació de l\'esdeveniment.',
        'required': False
    },
    {
        'name': 'eventurl',
        'message': '\u0036\u20E3 Envieu-me l\'*URL de l\'esdeveniment*.\n\nPodeu enviar /skip per a deixar el camp en blanc o /cancel per a cancel·lar el procés de creació de l\'esdeveniment.',
        'required': False
    },
    {
        'name': 'newsurl',
        'message': '\u0034\u20E3 Envieu-me l\'*URL de la notícia*.\n\nPodeu enviar /skip per a deixar el camp en blanc o /cancel per a cancel·lar el procés de creació de la notícia.',
        'required': False
    },
]


def parse_fields(field, value):
    if field == 'type':
        if value == 'Esdeveniment' or value == 'Notícia' or value == 'Paquets de llengua':  
             return value
        elif value == 'esdeveniment' or value == 'notícia' or value == 'paquets de llengua':
             valuecap = value.capitalize()  
             return valuecap
        else:
             error = 'error'
             return error
    if field == 'month':
        if value == 'Gener' or value == 'Febrer' or value == 'Març' or value == 'Abril' or value == 'Maig' or value == 'Juny' or value == 'Juliol' or value == 'Agost' or value == 'Setembre' or value == 'Octubre' or value == 'Novembre' or value == 'Desembre':  
             return value
        elif value == 'gener' or value == 'febrer' or value == 'març' or value == 'abril' or value == 'maig' or value == 'juny' or value == 'juliol' or value == 'agost' or value == 'setembre' or value == 'octubre' or value == 'novembre' or value == 'desembre':
             valuecap = value.capitalize()  
             return valuecap
        else:
             error = 'error'
             return error
    if field == 'day':
        try:
             value2 = int(value)
        except:
             error = 'error'
             return error
        if value2 >= 1 and value2 <= 31:
             return value
        else:
             error = 'error'
             return error
    if field == 'year':
        actualdate = datetime.now()
        actualyear = int(actualdate.year)
        try:
             value2 = int(value)
        except:
             error = 'error'
             return error
        if value2 >= actualyear and value2 <= actualyear + 3:
             return value
        else:
             error = 'error'
             return error
    if field == 'hour':
        try:
             value2 = int(value)
        except:
             error = 'error'
             return error
        if value2 >= 0 and value2 <= 23:
             return value
        else:
             error = 'error'
             return error
    if field == 'minute':
        try:
             value2 = int(value)
        except:
             error = 'error'
             return error
        if value2 >= 0 and value2 <= 59:
             return value
        else:
             error = 'error'
             return error
    if field == 'date':
        cal = parsedatetime.Calendar()
        time_struct, parse_status = cal.parse(value)
        timestamp = time.mktime(datetime(*time_struct[:6]).timetuple())
        return str(int(timestamp))
    if field == 'eventurl':
        try:
             assert url(value)
             return value
        except:
             error = 'error'
             return error
    if field == 'newsurl':
        try:
             assert url(value)
             return value
        except:
             error = 'error'
             return error
    return value


def help_command(bot, update):
    bot.sendMessage(update.message.chat_id, text='Aquest bot no és operatiu. Si cerqueu el paquet de llengua en català per al Telegram, aneu a @softcatala.')

def platform(bot, update):
    query = update.callback_query
    bot.editMessageText(text="Heu triat el paquet de llengua per la plataforma: %s" % query.data,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)
    bot.sendMessage(update.message.chat_id,
		    text="Aquí teniu el paquet. Apanyeu-se-les per insl·lar-lo 😝")
   bot.sendDocument(update.message.chat_id,
		    file_id="BQADBAADgBkAAgdxMQVGngQnfYvp7QI")
    #user_id = update.message.from_user.id
    platform_name= query.data
    writer = csv.writer(open("stats.csv", 'w'))
    writer.writerow([platform_name])

def download_command(bot, update):
    user_id = update.message.from_user.id
    # Replace USER_ID with your user_id number:
    if user_id == USER_ID:
        keyboard = [InlineKeyboardButton("Android", callback_data='Android'),
                     InlineKeyboardButton("iOS", callback_data='iOS'),
                    # [InlineKeyboardButton("Windows Phone", callback_data='WP'),
		  InlineKeyboardButton("Telegram Desktop", callback_data='tdesktop')]

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
    
class CommandsModule(object):
    def __init__(self):
        self.handlers = [
            CommandHandler('start', self.start_command, pass_args=True),
            CommandHandler('skip', self.skip_command),
	    CommandHandler('cancel', self.cancel_command),
            CommandHandler('help', help_command),
            CommandHandler('baixa', download_command),
            CallbackQueryHandler(platform),
            MessageHandler([Filters.text], self.message)
        ]
        self.store = TinyDBStore()

    def start_command(self, bot, update, args):
        user_id = update.message.from_user.id
        # Replace USER_ID with your user_id number:
        if user_id == USER_ID:
            self.store.new_draft(user_id)
            bot.sendMessage(update.message.chat_id,parse_mode='Markdown',
                        text="Crearem una publicació per a compartir.\n\n\u0031\u20E3 El primer que heu de fer és enviar-me el *nom de la publicació*.\n\nSi no voleu continuar amb el procés, envieu /cancel.",
                        reply_markup=ReplyKeyboardHide())
        else:
            f_name = update.message.from_user.first_name
            bot.sendMessage(update.message.chat_id,
                        parse_mode='Markdown',
                        text= str(f_name) + ", aquest bot no és operatiu. Si cerqueu el paquet de llengua en català per al Telegram, aneu a @softcatala.")

    def message(self, bot, update):
        user_id = update.message.from_user.id
        text = update.message.text
        draft = self.store.get_draft(user_id)

        if draft:
            event = draft['event']
            current_field = draft['current_field']
            field = FIELDS[current_field]

            event[field['name']] = parse_fields(field['name'], text)

            if field['name'] == 'type' and event['type'] == 'error':
                  bot.sendMessage(
                  update.message.chat_id,
                  text="\u26A0\uFE0F No és un tipus de publicació vàlid, escriviu-lo amb lletres i en català i torneu-ho a provar."
                  )
                  current_field += 0
                  self.update_draft(bot, event, user_id, update, current_field)
            elif field['name'] == 'description' and event['type'] == 'Notícia':
                  current_field += 9
                  self.update_draft(bot, event, user_id, update, current_field)
            elif field['name'] == 'eventurl' and event['eventurl'] != 'error':
                  current_field += 2
                  self.update_draft(bot, event, user_id, update, current_field)
            elif field['name'] == 'day' and event['day'] == 'error':
                  bot.sendMessage(
                  update.message.chat_id,
                  text="\u26A0\uFE0F No és un dia vàlid, assegureu-vos què és un nombre entre 1 i 31 i torneu-ho a provar."
                  )
                  current_field += 0
                  self.update_draft(bot, event, user_id, update, current_field)

            elif field['name'] == 'month' and event['month'] == 'error':
                  bot.sendMessage(
                  update.message.chat_id,
                  text="\u26A0\uFE0F No és un mes vàlid, escriviu-lo amb lletres i en català i torneu-ho a provar."
                  )
                  current_field += 0
                  self.update_draft(bot, event, user_id, update, current_field)

            elif field['name'] == 'year' and event['year'] == 'error':
                  actualdate = datetime.now()
                  actualyear = int(actualdate.year)
                  bot.sendMessage(
                  update.message.chat_id,
                  text="\u26A0\uFE0F No és un any vàlid, heu d'escriure " + str(actualyear) + ", " + str(actualyear + 1) + ", " + str(actualyear + 2) + " o " + str(actualyear + 3) + " i torneu-ho a provar."
                  )
                  current_field += 0
                  self.update_draft(bot, event, user_id, update, current_field)

            elif field['name'] == 'hour' and event['hour'] == 'error':
                  bot.sendMessage(
                  update.message.chat_id,
                  text="\u26A0\uFE0F No és una hora vàlida, assegureu-vos que és un nombre entre 0 i 23 i torneu-ho a provar."
                  )
                  current_field += 0
                  self.update_draft(bot, event, user_id, update, current_field)

            elif field['name'] == 'minute' and event['minute'] == 'error':
                  bot.sendMessage(
                  update.message.chat_id,
                  text="\u26A0\uFE0F No és un minut vàlid, assegureu-vos què és un nombre entre 0 i 59 i torneu-ho a provar."
                  )
                  current_field += 0
                  self.update_draft(bot, event, user_id, update, current_field)

            elif field['name'] == 'eventurl' and event['eventurl'] == 'error':
                  bot.sendMessage(
                  update.message.chat_id,
                  text="\u26A0\uFE0F Sembla que l'URL per a l\'esdeveniment que heu enviat no és vàlid, comproveu-lo i torneu-lo a enviar."
                  )
                  current_field += 0
                  self.update_draft(bot, event, user_id, update, current_field)

            elif field['name'] == 'newsurl' and event['newsurl'] == 'error':
                  bot.sendMessage(
                  update.message.chat_id,
                  text="\u26A0\uFE0F Sembla que l'URL per a la notícia que heu enviat no és vàlid, comproveu-lo i torneu-lo a enviar."
                  )
                  current_field += 0
                  self.update_draft(bot, event, user_id, update, current_field)

            else:
                  current_field += 1

                  self.update_draft(bot, event, user_id, update, current_field)

        else:
            bot.sendMessage(
            update.message.chat_id,
            parse_mode='Markdown',
            text="\U0001F914 No entenc el que em voleu dir, però sóc un robot \U0001F916 i encara no sóc en funcionament. Si cerqueu el paquet de llengua en català per al Telegram, aneu a @softcatala.",
            reply_markup=ReplyKeyboardHide()
            )

    def cancel_command(self, bot, update):
        user_id = update.message.from_user.id
        draft = self.store.get_draft(user_id)

        if draft:
            self.store.remove_draft(update.message.from_user.id)
            bot.sendMessage(
            update.message.chat_id,
            text="\U0001F5D1 S'ha cancel·lat la creació de la publicació.",
            reply_markup=ReplyKeyboardHide()
            )
        else:
            bot.sendMessage(
            update.message.chat_id,
            text="\u26A0\uFE0F No hi ha res a cancel·lar.\nAquesta comanda només funciona quan s'ha iniciat la creació d'una publicació.",
            reply_markup=ReplyKeyboardHide()
        )

    def skip_command(self, bot, update):
        user_id = update.message.from_user.id
        draft = self.store.get_draft(user_id)

        if draft:
            current_field = draft['current_field']
            field = FIELDS[current_field]

            if field['required']:
                bot.sendMessage(update.message.chat_id,parse_mode='Markdown',
                                text="\u26A0\uFE0F Aquest camp és necessari.\n\n" + field['message'])
            elif field['name'] == 'eventurl':
                event = draft['event']
                current_field += 2
                self.update_draft(bot, event, user_id, update, current_field)
            else:
                event = draft['event']
                current_field += 1
                self.update_draft(bot, event, user_id, update, current_field)

        else:
            bot.sendMessage(update.message.chat_id,
                            text="\u26A0\uFE0F Aquesta ordre només té sentit si s'està creant una publicació i es vol deixar en blanc un camp que no és necessari.")

    def update_draft(self, bot, event, user_id, update, current_field):
        self.store.update_draft(user_id, event, current_field)

        if current_field <= len(FIELDS) - 1:

            if FIELDS[current_field]['name'] == 'type':
                bot.sendMessage(
                    update.message.chat_id,
                    parse_mode='Markdown',
                    text=FIELDS[current_field]['message'],
                    reply_markup=ReplyKeyboardMarkup(
                         keyboard=[
                              ['Notícia'], ['Esdeveniment'],['Paquets de llengua']
                         ],
                         one_time_keyboard=True,
                         resize_keyboard=True
                ))

            elif FIELDS[current_field]['name'] == 'month':
                bot.sendMessage(
                    update.message.chat_id,
                    parse_mode='Markdown',
                    text=FIELDS[current_field]['message'],
                    reply_markup=ReplyKeyboardMarkup(
                         keyboard=[
                              ['Gener','Febrer','Març'], ['Abril','Maig','Juny'],['Juliol','Agost','Setembre'],['Octubre','Novembre','Desembre']
                         ],
                         one_time_keyboard=True,
                         resize_keyboard=True
                ))

            elif FIELDS[current_field]['name'] == 'day' and event['month'] == 'Febrer':
                bot.sendMessage(
                    update.message.chat_id,
                    parse_mode='Markdown',
                    text=FIELDS[current_field]['message'],
                    reply_markup=ReplyKeyboardMarkup(
                         keyboard=[
                              ['1','2','3','4'],['5','6','7','8'],['9','10','11','12'],['13','14','15','16'],['17','18','19','20'],['21','22','23','24'],['25','26','27','28'],['29']
                         ],
                         one_time_keyboard=True,
                         resize_keyboard=True
                ))

            elif FIELDS[current_field]['name'] == 'day' and event['month'] == 'Abril':
                bot.sendMessage(
                    update.message.chat_id,
                    parse_mode='Markdown',
                    text=FIELDS[current_field]['message'],
                    reply_markup=ReplyKeyboardMarkup(
                         keyboard=[
                              ['1','2','3','4'],['5','6','7','8'],['9','10','11','12'],['13','14','15','16'],['17','18','19','20'],['21','22','23','24'],['25','26','27','28'],['29','30']
                         ],
                         one_time_keyboard=True,
                         resize_keyboard=True
                ))


            elif FIELDS[current_field]['name'] == 'day' and event['month'] == 'Juny':
                bot.sendMessage(
                    update.message.chat_id,
                    parse_mode='Markdown',
                    text=FIELDS[current_field]['message'],
                    reply_markup=ReplyKeyboardMarkup(
                         keyboard=[
                              ['1','2','3','4'],['5','6','7','8'],['9','10','11','12'],['13','14','15','16'],['17','18','19','20'],['21','22','23','24'],['25','26','27','28'],['29','30']
                         ],
                         one_time_keyboard=True,
                         resize_keyboard=True
                ))


            elif FIELDS[current_field]['name'] == 'day' and event['month'] == 'Setembre':
                bot.sendMessage(
                    update.message.chat_id,
                    parse_mode='Markdown',
                    text=FIELDS[current_field]['message'],
                    reply_markup=ReplyKeyboardMarkup(
                         keyboard=[
                              ['1','2','3','4'],['5','6','7','8'],['9','10','11','12'],['13','14','15','16'],['17','18','19','20'],['21','22','23','24'],['25','26','27','28'],['29','30']
                         ],
                         one_time_keyboard=True,
                         resize_keyboard=True
                ))


            elif FIELDS[current_field]['name'] == 'day' and event['month'] == 'Novembre':
                bot.sendMessage(
                    update.message.chat_id,
                    parse_mode='Markdown',
                    text=FIELDS[current_field]['message'],
                    reply_markup=ReplyKeyboardMarkup(
                         keyboard=[
                              ['1','2','3','4'],['5','6','7','8'],['9','10','11','12'],['13','14','15','16'],['17','18','19','20'],['21','22','23','24'],['25','26','27','28'],['29','30']
                         ],
                         one_time_keyboard=True,
                         resize_keyboard=True
                ))

            elif FIELDS[current_field]['name'] == 'day':
                bot.sendMessage(
                    update.message.chat_id,
                    parse_mode='Markdown',
                    text=FIELDS[current_field]['message'],
                    reply_markup=ReplyKeyboardMarkup(
                         keyboard=[
                              ['1','2','3','4'],['5','6','7','8'],['9','10','11','12'],['13','14','15','16'],['17','18','19','20'],['21','22','23','24'],['25','26','27','28'],['29','30','31']
                         ],
                         one_time_keyboard=True,
                         resize_keyboard=True
                ))

            elif FIELDS[current_field]['name'] == 'year':
                now = datetime.now()
                now2 = int(now.year)
                now3 = str(now2)
                next1 = str(now2 + 1)
                next2 = str(now2 + 2)
                next3 = str(now2 + 3)
                bot.sendMessage(
                    update.message.chat_id,
                    parse_mode='Markdown',
                    text=FIELDS[current_field]['message'],
                    reply_markup=ReplyKeyboardMarkup(
                         keyboard=[
                              [now3],[next1],[next2],[next3]
                         ],
                         one_time_keyboard=True,
                         resize_keyboard=True
                ))

            elif FIELDS[current_field]['name'] == 'hour':
                bot.sendMessage(
                    update.message.chat_id,
                    parse_mode='Markdown',
                    text=FIELDS[current_field]['message'],
                    reply_markup=ReplyKeyboardMarkup(
                         keyboard=[
                              ['6','7','8','9'],['10','11','12','13'],['14','15','16','17'],['18','19','20','21'],['22','23','0','1'],['2','3','4','5']
                         ],
                         one_time_keyboard=True,
                         resize_keyboard=True
                ))

            elif FIELDS[current_field]['name'] == 'minute':
                bot.sendMessage(
                    update.message.chat_id,
                    parse_mode='Markdown',
                    text=FIELDS[current_field]['message'],
                    reply_markup=ReplyKeyboardMarkup(
                         keyboard=[
                              ['00','15'],['30','45']
                         ],
                         one_time_keyboard=True,
                         resize_keyboard=True
                ))

            elif FIELDS[current_field]['name'] == 'date':
                 day = event['day']
                 year = event['year']
                 hour = event['hour']
                 minute = event['minute']
                 if event['month'] == 'Gener':
                      monthnum = '1'
                 elif event['month'] == 'Febrer':
                      monthnum = '2'
                 elif event['month'] == 'Març':
                      monthnum = '3'
                 elif event['month'] == 'Abril':
                      monthnum = '4'
                 elif event['month'] == 'Maig':
                      monthnum = '5'
                 elif event['month'] == 'Juny':
                      monthnum = '6'
                 elif event['month'] == 'Juliol':
                      monthnum = '7'
                 elif event['month'] == 'Agost':
                      monthnum = '8'
                 elif event['month'] == 'Setembre':
                      monthnum = '9'
                 elif event['month'] == 'Octubre':
                      monthnum = '10'
                 elif event['month'] == 'Novembre':
                      monthnum = '11'
                 else:
                      monthnum = '12'
                 newdate = monthnum + "/" + day + "/" + year + " " + hour + ":" + minute
                 bot.sendMessage(
                    update.message.chat_id,
                    parse_mode='Markdown',
                    text=FIELDS[current_field]['message'],
                    reply_markup=ReplyKeyboardMarkup(
                         keyboard=[
                              [newdate]
                         ],
                         one_time_keyboard=True,
                         resize_keyboard=True
                ))

            elif FIELDS[current_field]['name'] != 'type' or FIELDS[current_field]['name'] != 'month' or FIELDS[current_field]['name'] != 'day' or FIELDS[current_field]['name'] != 'year' or FIELDS[current_field]['name'] != 'hour' or FIELDS[current_field]['name'] != 'minute' or FIELDS[current_field]['name'] != 'date':
                bot.sendMessage(
                    update.message.chat_id,
                    parse_mode='Markdown',
                    text=FIELDS[current_field]['message'],
                    reply_markup=ReplyKeyboardHide()
                )
        else:
            event['user_id'] = user_id
            self.create_event(bot, update, event)

    def create_event(self, bot, update, event):
        self.store.insert_event(event)
        self.store.remove_draft(update.message.from_user.id)

        keyboard = [[InlineKeyboardButton(text="Envia la publicació", switch_inline_query=event['name'])], []]
        bot.sendMessage(
            update.message.chat_id,
            text="S'ha creat la publicació",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
        )

    def get_handlers(self):
        return self.handlers

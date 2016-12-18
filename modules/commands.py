# -*- coding: utf-8 -*-

import time
import csv
from datetime import datetime

from parsedatetime import parsedatetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardHide
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from validators import url, ValidationFailure

from store import TinyDBStore

from config import allowed_users, paths, chats

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
        'message': '\u0034\u20E3 Ara m\'haureu d\'enviar la *data i hora* de l\'esdeveniment; o només la *data* si esteu actualitzant els paquets de llengua.\n\n\U0001F5D3 En primer lloc seleccioneu el *mes*:',
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
    {
        'name': 'date_version',
        'message': 'Comproveu que la data de la versió és correcta (seguint l\'ordre *dia/mes/any*) i si és així premeu el botó per a desar-la.\n\nPer a cancel·lar el procés envieu /cancel.',
        'required': True
    },
    {
        'name': 'android',
        'message': '\u0035\u20E3 Envieu-me el *fitxer del paquet de llengua per a Android*. Assegureu-vos que el fitxer s\'anomena *strings.xml*.\n\nPodeu enviar /skip si no teniu el fitxer del paquet de llengua per a Android actualitzat o /cancel per a cancel·lar el procés d\'actualització dels paquets de llengua.',
        'required': False
    },
    {
        'name': 'ios',
        'message': '\u0036\u20E3 Envieu-me el *fitxer del paquet de llengua per a iOS*. Assegureu-vos que el fitxer s\'anomena *Localizable-ios.strings*.\n\nPodeu enviar /skip si no teniu el fitxer del paquet de llengua per a iOS actualitzat o /cancel per a cancel·lar el procés d\'actualització dels paquets de llengua.',
        'required': False
    },
    {
        'name': 'tdesktop',
        'message': '\u0037\u20E3 Envieu-me el *fitxer del paquet de llengua per a Telegram Desktop*. Assegureu-vos que el fitxer s\'anomena *tdesktop.strings*.\n\nPodeu enviar /skip si no teniu el fitxer del paquet de llengua per a Telegram Desktop actualitzat o /cancel per a cancel·lar el procés d\'actualització dels paquets de llengua.',
        'required': False
    },
    {
        'name': 'validate',
        'message': '\u0038\u20E3 Comproveu que les dades són correctes i que rebeu els fitxers que heu actualitzat. Si no és així, premeu «No» i cancel·lareu l\'actualització dels paquets',
        'required': False
    },
]


def parse_fields(field, value):
    if field != 'android' and field != 'ios' and field != 'tdesktop':
        if value == '':
             error2 = 'error2'
             return error2
        else:
             if field == 'type':
                 if value == 'Esdeveniment' or value == 'Notícia':  
                      return value
                 if value == 'Paquets de llengua':
                      if '"type": "Paquets de llengua"' in open(paths['posts']+'event_drafts.json').read():
                           error3= 'error3'
                           return error3
                      else:
                           return value
                 elif value == 'esdeveniment' or value == 'notícia':
                      valuecap = value.capitalize()  
                      return valuecap
                 elif value == 'paquets de llengua':
                      if '"type": "Paquets de llengua"' in open(paths['posts']+'event_drafts.json').read():
                           error3= 'error3'
                           return error3
                      else:
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
                 if value2 >= actualyear - 1 and value2 <= actualyear + 3:
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
             if field == 'validate':
                 if value == 'Sí':
                      return value
                 elif value == 'No':
                      return value
                 else:
                      error = 'error'
                      return error
             return value
    elif field == 'android':
             f= open(paths['file_ids']+"draft_and_file_id.txt","r")
             and_file_id= f.read(32)
             f.close()
             if and_file_id == '--------------------------------':
                  and_file_id= 'NOT'
                  return str(and_file_id)
             else:
                  return str(and_file_id)
    elif field == 'ios':
             f= open(paths['file_ids']+"draft_ios_file_id.txt","r")
             ios_file_id= f.read(32)
             f.close()
             if ios_file_id == '--------------------------------':
                  ios_file_id= 'NOT'
                  return str(ios_file_id)
             else:
                  return str(ios_file_id)
    elif field == 'tdesktop':
             f= open(paths['file_ids']+"draft_tdesk_file_id.txt","r")
             tdesk_file_id= f.read(32)
             f.close()
             if tdesk_file_id == '--------------------------------':
                  tdesk_file_id= 'NOT'
                  return str(tdesk_file_id)
             else:
                  return str(tdesk_file_id)

def help_command(bot, update):
    bot.sendMessage(update.message.chat_id, text='Aquest bot no és operatiu. Si cerqueu el paquet de llengua en català per al Telegram, aneu a @softcatala.')

class CommandsModule(object):
    def __init__(self):
        self.handlers = [
            CommandHandler('post', self.start_command, pass_args=True),
            CommandHandler('admin', self.admin_command),
            CommandHandler('skip', self.skip_command),
	    CommandHandler('cancel', self.cancel_command),
            CommandHandler('help', help_command),
            CommandHandler('hello', self.hello_command),
            MessageHandler([Filters.text,Filters.document], self.message)
        ]
        self.store = TinyDBStore()

    def start_command(self, bot, update, args):
        user_id = update.message.from_user.id
        chat= str(update.message.chat_id)
        if str(user_id) in allowed_users.values() and chat != chats['group']:
            self.store.new_draft(user_id)
            bot.sendMessage(update.message.chat_id,parse_mode='Markdown',
                        text="Crearem una publicació per a compartir.\n\n\u0031\u20E3 El primer que heu de fer és enviar-me el *nom de la publicació*.\n\nSi no voleu continuar amb el procés, envieu /cancel.",
                        reply_markup=ReplyKeyboardHide())
        else:
            f_name = update.message.from_user.first_name
            chat= str(update.message.chat_id)
            if chat != chats['group']:
                 bot.sendMessage(update.message.chat_id,
                             parse_mode='Markdown',
                             text= str(f_name) + ", aquest bot no és operatiu. Si cerqueu el paquet de llengua en català per al Telegram, aneu a @softcatala.")
            else:
                 bot.sendMessage(update.message.chat_id,
                             parse_mode='Markdown',
                             text= "No es permet crear publicacions des del grup.")

    def hello_command(self, bot, update):
        user_id = update.message.from_user.id
        if str(user_id) in allowed_users.values():
            bot.sendMessage(chat_id= chats['group'], text='Hello world!')

    def admin_command(self, bot, update):
        user_id = update.message.from_user.id
        if str(user_id) in allowed_users.values():
            bot.sendMessage(update.message.chat_id,parse_mode='Markdown',
                        text="Sou administrador i podeu utilitzar les comandes:\n\n/post\n/stats\n\nI per ara ja està",
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

            if event['name'] == 'error2':
                        bot.sendMessage(
                        update.message.chat_id,
                        text="\u26A0\uFE0F No podeu deixar el nom de la publicació en blanc ni enviar un document. Torneu a provar-ho."
                        )
                        current_field += 0
                        self.update_draft(bot, event, user_id, update, current_field)
            elif field['name'] == 'type' and event['type'] == 'error2':
                        bot.sendMessage(
                        update.message.chat_id,
                        text="\u26A0\uFE0F No podeu deixar el tipus de publicació en blanc ni enviar un document. Torneu a provar-ho, amb els botons ho teniu fàcil \U0001F609."
                        )
                        current_field += 0
                        self.update_draft(bot, event, user_id, update, current_field)
            elif field['name'] == 'type' and event['type'] == 'error':
                        bot.sendMessage(
                        update.message.chat_id,
                        text="\u26A0\uFE0F No és un tipus de publicació vàlid, escriviu-lo amb lletres i en català i torneu a provar-ho, amb els botons ho teniu fàcil \U0001F609."
                        )
                        current_field += 0
                        self.update_draft(bot, event, user_id, update, current_field)
            elif field['name'] == 'type' and event['type'] == 'error3':
                        bot.sendMessage(
                        update.message.chat_id,
                        text="\u26A0\uFE0F No es permet que més d'un usuari realitzi aquesta acció al mateix temps... Com és evident, algun dels administradors se us ha avançat.\n\nNo tinc més remei que cancel·lar l'actualització dels paquets."
                        )
                        self.cancel_command(bot, update)
            elif field['name'] == 'description' and event['description'] == 'error2':
                        bot.sendMessage(
                        update.message.chat_id,
                        text="\u26A0\uFE0F No podeu deixar la descripció en blanc ni enviar un document. Torneu a provar-ho."
                        )
                        current_field += 0
                        self.update_draft(bot, event, user_id, update, current_field)
            elif field['name'] == 'description' and event['type'] == 'Notícia':
                  current_field += 9
                  self.update_draft(bot, event, user_id, update, current_field)
            elif field['name'] == 'month' and event['month'] == 'error2':
                        bot.sendMessage(
                        update.message.chat_id,
                        text="\u26A0\uFE0F No podeu deixar el mes en blanc ni enviar un document. Torneu a provar-ho, amb els botons ho teniu fàcil \U0001F609."
                        )
                        current_field += 0
                        self.update_draft(bot, event, user_id, update, current_field)
            elif field['name'] == 'day' and event['day'] == 'error2':
                        bot.sendMessage(
                        update.message.chat_id,
                        text="\u26A0\uFE0F No podeu deixar el dia en blanc ni enviar un document. Torneu a provar-ho, amb els botons ho teniu fàcil \U0001F609."
                        )
                        current_field += 0
                        self.update_draft(bot, event, user_id, update, current_field)
            elif field['name'] == 'year' and event['year'] == 'error2':
                        bot.sendMessage(
                        update.message.chat_id,
                        text="\u26A0\uFE0F No podeu deixar l'any en blanc ni enviar un document. Torneu a provar-ho, amb els botons ho teniu fàcil \U0001F609."
                        )
                        current_field += 0
                        self.update_draft(bot, event, user_id, update, current_field)
            elif field['name'] == 'hour' and event['hour'] == 'error2':
                        bot.sendMessage(
                        update.message.chat_id,
                        text="\u26A0\uFE0F No podeu deixar l'hora en blanc ni enviar un document. Torneu a provar-ho, amb els botons ho teniu fàcil \U0001F609."
                        )
                        current_field += 0
                        self.update_draft(bot, event, user_id, update, current_field)
            elif field['name'] == 'minute' and event['minute'] == 'error2':
                        bot.sendMessage(
                        update.message.chat_id,
                        text="\u26A0\uFE0F No podeu deixar els minuts en blanc ni enviar un document. Torneu a provar-ho, amb els botons ho teniu fàcil \U0001F609."
                        )
                        current_field += 0
                        self.update_draft(bot, event, user_id, update, current_field)
            elif field['name'] == 'date' and event['date'] == 'error2':
                        bot.sendMessage(
                        update.message.chat_id,
                        text="\u26A0\uFE0F No podeu deixar la data en blanc ni enviar un document. Només heu de prémer el botó si la data és correcta."
                        )
                        current_field += 0
                        self.update_draft(bot, event, user_id, update, current_field)
            elif field['name'] == 'place' and event['place'] == 'error2':
                        bot.sendMessage(
                        update.message.chat_id,
                        text="\u26A0\uFE0F No podeu deixar el lloc de l'esdeveniment en blanc ni enviar un document. Torneu a provar-ho."
                        )
                        current_field += 0
                        self.update_draft(bot, event, user_id, update, current_field)
            elif field['name'] == 'eventurl' and event['eventurl'] == 'error2':
                        bot.sendMessage(
                        update.message.chat_id,
                        text="\u26A0\uFE0F No podeu deixar l'URL de l'esdeveniment en blanc ni enviar un document. Torneu a provar-ho."
                        )
                        current_field += 0
                        self.update_draft(bot, event, user_id, update, current_field)
            elif field['name'] == 'newsurl' and event['newsurl'] == 'error2':
                        bot.sendMessage(
                        update.message.chat_id,
                        text="\u26A0\uFE0F No podeu deixar l'URL de la notícia en blanc ni enviar un document. Torneu a provar-ho."
                        )
                        current_field += 0
                        self.update_draft(bot, event, user_id, update, current_field)
            elif field['name'] == 'date_version' and event['date_version'] == 'error2':
                        bot.sendMessage(
                        update.message.chat_id,
                        text="\u26A0\uFE0F No podeu deixar la data de la versió dels paquets en blanc ni enviar un document. Només heu de prémer el botó si la data és correcta."
                        )
                        current_field += 0
                        self.update_draft(bot, event, user_id, update, current_field)
            elif field['name'] == 'year' and event['type'] == 'Paquets de llengua':
                  current_field += 7
                  self.update_draft(bot, event, user_id, update, current_field)
            elif field['name'] == 'eventurl' and event['eventurl'] != 'error' and event['eventurl'] != 'error2':
                  current_field += 7
                  self.update_draft(bot, event, user_id, update, current_field)
            elif field['name'] == 'newsurl' and event['newsurl'] != 'error' and event['newsurl'] != 'error2':
                  current_field += 6
                  self.update_draft(bot, event, user_id, update, current_field)
            elif field['name'] == 'day' and event['day'] == 'error':
                  bot.sendMessage(
                  update.message.chat_id,
                  text="\u26A0\uFE0F No és un dia vàlid, assegureu-vos què és un nombre entre 1 i 31 i torneu a provar-ho."
                  )
                  current_field += 0
                  self.update_draft(bot, event, user_id, update, current_field)

            elif field['name'] == 'month' and event['month'] == 'error':
                  bot.sendMessage(
                  update.message.chat_id,
                  text="\u26A0\uFE0F No és un mes vàlid, escriviu-lo amb lletres i en català i torneu a provar-ho."
                  )
                  current_field += 0
                  self.update_draft(bot, event, user_id, update, current_field)

            elif field['name'] == 'year' and event['year'] == 'error':
                  actualdate = datetime.now()
                  actualyear = int(actualdate.year)
                  bot.sendMessage(
                  update.message.chat_id,
                  text="\u26A0\uFE0F No és un any vàlid, heu d'escriure " + str(actualyear) + ", o algun dels anys que apareixen als botons, i torneu a provar-ho."
                  )
                  current_field += 0
                  self.update_draft(bot, event, user_id, update, current_field)

            elif field['name'] == 'hour' and event['hour'] == 'error':
                  bot.sendMessage(
                  update.message.chat_id,
                  text="\u26A0\uFE0F No és una hora vàlida, assegureu-vos que és un nombre entre 0 i 23 i torneu a provar-ho."
                  )
                  current_field += 0
                  self.update_draft(bot, event, user_id, update, current_field)

            elif field['name'] == 'minute' and event['minute'] == 'error':
                  bot.sendMessage(
                  update.message.chat_id,
                  text="\u26A0\uFE0F No és un minut vàlid, assegureu-vos què és un nombre entre 0 i 59 i torneu a provar-ho."
                  )
                  current_field += 0
                  self.update_draft(bot, event, user_id, update, current_field)

            elif field['name'] == 'eventurl' and event['eventurl'] == 'error':
                  bot.sendMessage(
                  update.message.chat_id,
                  text="\u26A0\uFE0F Sembla que l'URL per a l\'esdeveniment que heu enviat no és vàlid, comproveu-lo i torneu a enviar-lo."
                  )
                  current_field += 0
                  self.update_draft(bot, event, user_id, update, current_field)

            elif field['name'] == 'newsurl' and event['newsurl'] == 'error':
                  bot.sendMessage(
                  update.message.chat_id,
                  text="\u26A0\uFE0F Sembla que l'URL per a la notícia que heu enviat no és vàlid, comproveu-lo i torneu a enviar-lo."
                  )
                  current_field += 0
                  self.update_draft(bot, event, user_id, update, current_field)

            elif field['name'] == 'validate' and event['validate'] == 'error':
                  bot.sendMessage(
                  update.message.chat_id,
                  text="\u26A0\uFE0F No és gaire difícil... «Sí» o «No»."
                  )
                  current_field += 0
                  self.update_draft(bot, event, user_id, update, current_field)

            elif field['name'] == 'android':
                  file_name = update.message.document.file_name
                  file_id = update.message.document.file_id
                  if file_name != 'strings.xml':
                        bot.sendMessage(
                        update.message.chat_id,
                        parse_mode='Markdown',
                        text="\u26A0\uFE0F Heu enviat un fitxer de paquet de llengua per a Android que *no s'anomena strings.xml*. Comproveu que el fitxer és correcte i torneu a enviar-lo."
                        )
                        current_field += 0
                        self.update_draft(bot, event, user_id, update, current_field)
                  elif file_name == 'strings.xml':
                        bot.sendMessage(
                        update.message.chat_id,
                        parse_mode='Markdown',
                        text="\U0001F4E5 S'ha desat el fitxer de paquet de llengua per a Android anomenat strings.xml amb l'identificador _" + file_id + "_."
                        )
                        f=open(paths['file_ids']+'draft_and_file_id.txt','w')
                        f.write(file_id)
                        f.close()
                        event[field['name']] = parse_fields(field['name'], text)
                        android_version= event['date_version']
                        f=open(paths['versions']+'draft_and_version.txt','w')
                        f.write(android_version)
                        f.close()
                        current_field += 1
                        self.update_draft(bot, event, user_id, update, current_field)

            elif field['name'] == 'ios':
                  file_name = update.message.document.file_name
                  file_id = update.message.document.file_id
                  if file_name != 'Localizable-ios.strings':
                        bot.sendMessage(
                        update.message.chat_id,
                        parse_mode='Markdown',
                        text="\u26A0\uFE0F Heu enviat un fitxer de paquet de llengua per a iOS que *no s'anomena Localizable-ios.strings*. Comproveu que el fitxer és correcte i torneu a enviar-lo."
                        )
                        current_field += 0
                        self.update_draft(bot, event, user_id, update, current_field)
                  elif file_name == 'Localizable-ios.strings':
                        bot.sendMessage(
                        update.message.chat_id,
                        parse_mode='Markdown',
                        text="\U0001F4E5 S'ha desat el fitxer de paquet de llengua per a iOS anomenat Localizable-ios.strings amb l'identificador _" + file_id + "_."
                        )
                        f=open(paths['file_ids']+'draft_ios_file_id.txt','w')
                        f.write(file_id)
                        f.close()
                        event[field['name']] = parse_fields(field['name'], text)
                        ios_version= event['date_version']
                        f=open(paths['versions']+'draft_ios_version.txt','w')
                        f.write(ios_version)
                        f.close()
                        current_field += 1
                        self.update_draft(bot, event, user_id, update, current_field)

            elif field['name'] == 'tdesktop':
                  file_name = update.message.document.file_name
                  file_id = update.message.document.file_id
                  if file_name != 'tdesktop.strings':
                        bot.sendMessage(
                        update.message.chat_id,
                        parse_mode='Markdown',
                        text="\u26A0\uFE0F Heu enviat un fitxer de paquet de llengua per a Telegram Desktop que *no s'anomena tdesktop.strings*. Comproveu que el fitxer és correcte i torneu a enviar-lo."
                        )
                        current_field += 0
                        self.update_draft(bot, event, user_id, update, current_field)
                  elif file_name == 'tdesktop.strings':
                        bot.sendMessage(
                        update.message.chat_id,
                        parse_mode='Markdown',
                        text="\U0001F4E5 S'ha desat el fitxer de paquet de llengua per a Telegram Desktop anomenat tdesktop.strings amb l'identificador _" + file_id + "_."
                        )
                        f=open(paths['file_ids']+'draft_tdesk_file_id.txt','w')
                        f.write(file_id)
                        f.close()
                        event[field['name']] = parse_fields(field['name'], text)
                        tdesk_version= event['date_version']
                        f=open(paths['versions']+'draft_tdesk_version.txt','w')
                        f.write(tdesk_version)
                        f.close()
                        current_field += 1
                        self.update_draft(bot, event, user_id, update, current_field)

            else:
                  current_field += 1
                  self.update_draft(bot, event, user_id, update, current_field)

        else:
            chat= str(update.message.chat_id)
            if chat != chats['group']:
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
            elif field['name'] == 'android':
                event = draft['event']
                android_version= 'Not updated'
                f=open(paths['versions']+'draft_and_version.txt','w')
                f.write(android_version)
                f.close()
                file_id= '--------------------------------'
                f=open(paths['file_ids']+'draft_and_file_id.txt','w')
                f.write(file_id)
                f.close()
                value= 'null'
                event[field['name']] = parse_fields(field['name'], value)
                current_field += 1
                self.update_draft(bot, event, user_id, update, current_field)
            elif field['name'] == 'ios':
                event = draft['event']
                ios_version= 'Not updated'
                f=open(paths['versions']+'draft_ios_version.txt','w')
                f.write(ios_version)
                f.close()
                file_id= '--------------------------------'
                f=open(paths['file_ids']+'draft_ios_file_id.txt','w')
                f.write(file_id)
                f.close()
                value= 'null'
                event[field['name']] = parse_fields(field['name'], value)
                current_field += 1
                self.update_draft(bot, event, user_id, update, current_field)
            elif field['name'] == 'tdesktop':
                event = draft['event']
                tdesk_version= 'Not updated'
                f=open(paths['versions']+'draft_tdesk_version.txt','w')
                f.write(tdesk_version)
                f.close()
                file_id= '--------------------------------'
                f=open(paths['file_ids']+'draft_tdesk_file_id.txt','w')
                f.write(file_id)
                f.close()
                value= 'null'
                event[field['name']] = parse_fields(field['name'], value)
                current_field += 1
                self.update_draft(bot, event, user_id, update, current_field)
            elif field['name'] == 'eventurl':
                event = draft['event']
                current_field += 7
                self.update_draft(bot, event, user_id, update, current_field)
            elif field['name'] == 'newsurl':
                event = draft['event']
                current_field += 6
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
                              ['Notícia'],['Esdeveniment'],['Paquets de llengua']
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

            elif FIELDS[current_field]['name'] == 'year' and event['type'] == 'Esdeveniment':
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

            elif FIELDS[current_field]['name'] == 'year' and event['type'] == 'Paquets de llengua':
                now = datetime.now()
                now2 = int(now.year)
                now3 = str(now2)
                preyear = str(now2 - 1)
                bot.sendMessage(
                    update.message.chat_id,
                    parse_mode='Markdown',
                    text=FIELDS[current_field]['message'],
                    reply_markup=ReplyKeyboardMarkup(
                         keyboard=[
                              [preyear],[now3]
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

            elif FIELDS[current_field]['name'] == 'date_version':
                 if int(event['day']) > 9:
                      day = event['day']
                 else:
                      day = '0' + event['day']
                 year = event['year']
                 if event['month'] == 'Gener':
                      monthnum = '01'
                 elif event['month'] == 'Febrer':
                      monthnum = '02'
                 elif event['month'] == 'Març':
                      monthnum = '03'
                 elif event['month'] == 'Abril':
                      monthnum = '04'
                 elif event['month'] == 'Maig':
                      monthnum = '05'
                 elif event['month'] == 'Juny':
                      monthnum = '06'
                 elif event['month'] == 'Juliol':
                      monthnum = '07'
                 elif event['month'] == 'Agost':
                      monthnum = '08'
                 elif event['month'] == 'Setembre':
                      monthnum = '09'
                 elif event['month'] == 'Octubre':
                      monthnum = '10'
                 elif event['month'] == 'Novembre':
                      monthnum = '11'
                 else:
                      monthnum = '12'
                 newdate = day + "/" + monthnum + "/" + year
                 draftverstxt=open(paths['versions']+'draft_cur_version.txt','w')
                 draftverstxt.write(newdate)
                 draftverstxt.close()
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

            elif FIELDS[current_field]['name'] == 'validate':
                if event['android'] != 'NOT':
                     f= open(paths['file_ids']+"draft_and_file_id.txt","r")
                     and_file_id= f.read(32)
                     f.close()
                     f= open(paths['versions']+"draft_and_version.txt","r")
                     and_version= f.read(10)
                     f.close()
                     emoji_and= '\u2705 '
                else:
                     f= open(paths['versions']+"android_version.txt","r")
                     and_version= f.read(10)
                     f.close()
                     emoji_and= '\u274C '
                if event['ios'] != 'NOT':
                     f= open(paths['file_ids']+"draft_ios_file_id.txt","r")
                     ios_file_id= f.read(32)
                     f.close()
                     f= open(paths['versions']+"draft_ios_version.txt","r")
                     ios_version= f.read(10)
                     f.close()
                     emoji_ios= '\u2705 '
                else:
                     f= open(paths['versions']+"ios_version.txt","r")
                     ios_version= f.read(10)
                     f.close()
                     emoji_ios= '\u274C '
                if event['tdesktop'] != 'NOT':
                     f= open(paths['file_ids']+"draft_tdesk_file_id.txt","r")
                     tdesk_file_id= f.read(32)
                     f.close()
                     f= open(paths['versions']+"draft_tdesk_version.txt","r")
                     tdesk_version= f.read(10)
                     f.close()
                     emoji_tdesk= '\u2705 '
                else:
                     f= open(paths['versions']+"tdesktop_version.txt","r")
                     tdesk_version= f.read(10)
                     f.close()
                     emoji_tdesk= '\u274C '
                bot.sendMessage(
                    update.message.chat_id,
                    parse_mode='Markdown',
                    text=FIELDS[current_field]['message'] + '\n\nHeu actualitzat:\n\n' + emoji_and + 'Android: ' + and_version + '\n' + emoji_ios + 'iOS: ' + ios_version + '\n' + emoji_tdesk + 'Telegram Desktop: ' + tdesk_version + '.\n',
                    reply_markup=ReplyKeyboardMarkup(
                         keyboard=[
                              ['Sí','No']
                         ],
                         one_time_keyboard=True,
                         resize_keyboard=True
                ))
                if event['android'] != 'NOT':
                      bot.sendDocument(chat_id=update.message.chat_id,
                            document=and_file_id)
                if event['ios'] != 'NOT':
                      bot.sendDocument(chat_id=update.message.chat_id,
                            document=ios_file_id)
                if event['tdesktop'] != 'NOT':
                      bot.sendDocument(chat_id=update.message.chat_id,
                            document=tdesk_file_id)

            elif FIELDS[current_field]['name'] != 'type' or FIELDS[current_field]['name'] != 'month' or FIELDS[current_field]['name'] != 'day' or FIELDS[current_field]['name'] != 'year' or FIELDS[current_field]['name'] != 'hour' or FIELDS[current_field]['name'] != 'minute' or FIELDS[current_field]['name'] != 'date' or FIELDS[current_field]['name'] != 'date_version' or FIELDS[current_field]['name'] != 'validate':
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
        if event['type'] == 'Paquets de llengua' and event['validate'] == 'No':
            self.cancel_command(bot, update)
        elif event['type'] == 'Paquets de llengua' and event['validate'] == 'Sí':
             if event['android'] == 'NOT' and event['ios'] == 'NOT' and event['tdesktop'] == 'NOT':
                 bot.sendMessage(
                      update.message.chat_id,
                      text="No té sentit generar l'actualització de paquets si no n'heu actualitzat cap. Procediré amb la cancel·lació de l'actualització de paquets.",
                      reply_markup=ReplyKeyboardHide()
                      )
                 self.cancel_command(bot, update)
             else:
                 if event['type'] == 'Paquets de llengua':
                      #SAVE DATA IN TXT FILES
                      if int(event['day']) > 9:
                           day = event['day']
                      else:
                           day = '0' + event['day']
                      year = event['year']
                      if event['month'] == 'Gener':
                           monthnum = '01'
                      elif event['month'] == 'Febrer':
                           monthnum = '02'
                      elif event['month'] == 'Març':
                           monthnum = '03'
                      elif event['month'] == 'Abril':
                           monthnum = '04'
                      elif event['month'] == 'Maig':
                           monthnum = '05'
                      elif event['month'] == 'Juny':
                           monthnum = '06'
                      elif event['month'] == 'Juliol':
                           monthnum = '07'
                      elif event['month'] == 'Agost':
                           monthnum = '08'
                      elif event['month'] == 'Setembre':
                           monthnum = '09'
                      elif event['month'] == 'Octubre':
                           monthnum = '10'
                      elif event['month'] == 'Novembre':
                           monthnum = '11'
                      else:
                           monthnum = '12'
                      newdate = day + "/" + monthnum + "/" + year
                      versiontxt=open(paths['versions']+'current_version.txt','w')
                      versiontxt.write(newdate)
                      versiontxt.close()
                      if event['android'] != 'NOT':
                           f= open(paths['file_ids']+'draft_and_file_id.txt','r')
                           and_file_id= f.read(32)
                           f.close()
                           f=open(paths['file_ids']+'android_file_id.txt','w')
                           f.write(and_file_id)
                           f.close()
                           f= open(paths['versions']+'draft_and_version.txt','r')
                           and_version= f.read(10)
                           f.close()
                           f=open(paths['versions']+'android_version.txt','w')
                           f.write(and_version)
                           f.close()
                      if event['ios'] != 'NOT':
                           f= open(paths['file_ids']+'draft_ios_file_id.txt','r')
                           ios_file_id= f.read(32)
                           f.close()
                           f=open(paths['file_ids']+'ios_file_id.txt','w')
                           f.write(ios_file_id)
                           f.close()
                           f= open(paths['versions']+'draft_ios_version.txt','r')
                           ios_version= f.read(10)
                           f.close()
                           f=open(paths['versions']+'ios_version.txt','w')
                           f.write(ios_version)
                           f.close()
                      if event['tdesktop'] != 'NOT':
                           f= open(paths['file_ids']+'draft_tdesk_file_id.txt','r')
                           tdesk_file_id= f.read(32)
                           f.close()
                           f=open(paths['file_ids']+'tdesktop_file_id.txt','w')
                           f.write(tdesk_file_id)
                           f.close()
                           f= open(paths['versions']+'draft_tdesk_version.txt','r')
                           tdesk_version= f.read(10)
                           f.close()
                           f=open(paths['versions']+'tdesktop_version.txt','w')
                           f.write(tdesk_version)
                           f.close()
                      #SEND MESSAGE TO GROUP
                      f= open(paths['versions']+"android_version.txt","r")
                      and_version= f.read(10)
                      f.close()
                      if event['android'] != 'NOT':
                           f= open(paths['file_ids']+"android_file_id.txt","r")
                           and_file_id= f.read(32)
                           f.close()
                           emoji_and= '\u2705 '
                      else:
                           emoji_and= '\u274C '
                      f= open(paths['versions']+"ios_version.txt","r")
                      ios_version= f.read(10)
                      f.close()
                      if event['ios'] != 'NOT':
                           f= open(paths['file_ids']+"ios_file_id.txt","r")
                           ios_file_id= f.read(32)
                           f.close()
                           emoji_ios= '\u2705 '
                      else:
                           emoji_ios= '\u274C '
                      f= open(paths['versions']+"tdesktop_version.txt","r")
                      tdesk_version= f.read(10)
                      f.close()
                      if event['tdesktop'] != 'NOT':
                           f= open(paths['file_ids']+"tdesktop_file_id.txt","r")
                           tdesk_file_id= f.read(32)
                           f.close()
                           emoji_tdesk= '\u2705 '
                      else:
                           emoji_tdesk= '\u274C '
                      f_name = update.message.from_user.first_name
                      bot.sendMessage(
                          chat_id= chats['group'],
                          parse_mode='Markdown',
                          text= '*' + str(f_name) + '* ha actualitzat els paquets de llengua:\n\n' + emoji_and + 'Android: ' + and_version + '\n' + emoji_ios + 'iOS: ' + ios_version + '\n' + emoji_tdesk + 'Telegram Desktop: ' + tdesk_version + '.\n\nLa publicació s\'ha desat amb el nom *«' + event['name'] + '»*.'
                      )
                      if event['android'] != 'NOT':
                            bot.sendDocument(chat_id= chats['group'],
                                  document=and_file_id)
                      if event['ios'] != 'NOT':
                            bot.sendDocument(chat_id= chats['group'],
                                  document=ios_file_id)
                      if event['tdesktop'] != 'NOT':
                            bot.sendDocument(chat_id= chats['group'],
                                  document=tdesk_file_id)
        elif event['type'] == 'Esdeveniment':
             f_name = update.message.from_user.first_name
             bot.sendMessage(
                 chat_id= chats['group'],
                 parse_mode='Markdown',
                 text= '*' + str(f_name) + '* ha creat l\'esdeveniment *«' + event['name'] + '»* amb data ' + event['day'] + ' de ' + event['month'] + ' de ' + event['year'] + '.'
             )
        elif event['type'] == 'Notícia':
             f_name = update.message.from_user.first_name
             bot.sendMessage(
                 chat_id= chats['group'],
                 parse_mode='Markdown',
                 text= '*' + str(f_name) + '* ha creat la notícia *«' + event['name'] + '»*.'
             )
        self.store.insert_event(event)
        self.store.remove_draft(update.message.from_user.id)

        keyboard = [[InlineKeyboardButton(text="Envia la publicació", switch_inline_query=event['name'])], []]

        if event['type'] == 'Paquets de llengua':
              bot.sendMessage(
                    update.message.chat_id,
                    text="S'ha acabat l'actualització dels paquets de llengua",
                    reply_markup=ReplyKeyboardHide()
                    )

        bot.sendMessage(
        update.message.chat_id,
        text="S'ha creat la publicació",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
        )

    def get_handlers(self):
        return self.handlers

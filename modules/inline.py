# -*- coding: utf-8 -*-
import base64
import datetime
import locale
import json
import csv
from six.moves import urllib

from telegram import InlineQueryResultArticle, InlineQueryResultCachedDocument, ParseMode, \
    InputTextMessageContent, InputMessageContent, InlineKeyboardButton, InlineKeyboardMarkup, Emoji
from telegram.ext import InlineQueryHandler, CallbackQueryHandler

from store import TinyDBStore

from config import allowed_users, paths, inline_status


def create_event_payload(event):
    event_string = json.dumps(event)
    eight_bit_string = base64.b64encode(event_string.encode('ascii'))
    return urllib.parse.quote(eight_bit_string.decode('ascii'))

def create_keyboard(event, user):
    if event.get('type') and event['type'] == 'Esdeveniment':
          button = [
              InlineKeyboardButton(
                  text="\U0001F465 Afegeix-m'hi / treu-me'n",
                  callback_data='go_' + str(event.eid)
              )
          ]

          buttons = [
              InlineKeyboardButton(
                  text="\U0001F4C6 Calendari",
                  url='https://gent.softcatala.org/albert/softcatalabot/add.html#' + create_event_payload(event)
              )
          ]

          if event.get('eventurl'):
              buttons.append(InlineKeyboardButton(
                  text="\u2139\uFE0F Informació",
                  url=event.get('eventurl')
              ))

          return [button, buttons, []]

    if event.get('type') and event['type'] == 'Notícia':
  
          likes= 0
          if 'users' in event and len(event['users']) > 0:
              for u in event['users']:
                  if u['like'] == 1:
                       likes += u['like']
          nolikes= 0
          rawnolikes= 0
          if 'users' in event and len(event['users']) > 0:
              for u in event['users']:
                  if u['like'] == 2:
                       rawnolikes += u['like']
                       nolikes = int(rawnolikes / 2)           
          
          buttons = [
              InlineKeyboardButton(
                  text= str(likes) + " \U0001F44D\U0001F3FC",
                  callback_data='like_' + str(event.eid)
              ),
              InlineKeyboardButton(
                  text= str(nolikes) + " \U0001F44E\U0001F3FC",
                  callback_data='nolike_' + str(event.eid)
              )
          ]

          if event.get('newsurl'):
              buttons.append(InlineKeyboardButton(
                  text="\U0001F4F0",
                  url=event.get('newsurl')
              ))

          return [buttons, []]

    if event.get('type') and event['type'] == 'Paquets de llengua':
          if event.get('android') and event['android'] == 'NOT':
               f= open(paths['versions']+"android_version.txt","r")
               android_date= f.read(10)
               f.close()
               old_and= ' (' + android_date + ')'
          else:
               old_and= ''
          if event.get('ios') and event['ios'] == 'NOT':
               f= open(paths['versions']+"ios_version.txt","r")
               ios_date= f.read(10)
               f.close()
               old_ios= ' (' + ios_date + ')'
          else:
               old_ios= ''
          if event.get('tdesktop') and event['tdesktop'] == 'NOT':
               f= open(paths['versions']+"tdesktop_version.txt","r")
               tdesktop_date= f.read(10)
               f.close()
               old_tdesk= ' (' + tdesktop_date + ')'
          else:
               old_tdesk= ''
          button1 = [
              InlineKeyboardButton(
                  text="Android" + old_and,
                  url='http://telegram.me/Softcatalabot?start=android-channel'
              )
          ]
          button2 = [
              InlineKeyboardButton(
                  text="iOS" + old_ios,
                  url='http://telegram.me/Softcatalabot?start=ios-channel'
              )
          ]
          button3 = [
              InlineKeyboardButton(
                  text="TDesktop" + old_tdesk,
                  url='http://telegram.me/Softcatalabot?start=tdesktop-channel'
              )
          ]

          return [button1, button2, button3, []]


def format_date(param):
    locale.setlocale(locale.LC_TIME, "ca_ES.utf8")
    timestamp = int(param)
    date = datetime.datetime.fromtimestamp(timestamp)
    return date.strftime("%A, %d %B %Y a les %H.%M hores")

def create_event_message(event, user):
    if 'type' in event and event['type'] == 'Esdeveniment':
          message_text = "*{name}*\n{date}\n".format(
              name=event['name'],
              date=format_date(event['date'])
          )

          if 'description' in event:
              message_text += '\n_' + event['description'] + '_\n'

          if 'place' in event:
              message_text += '\n' + Emoji.ROUND_PUSHPIN + ' ' + event['place'] + ' [(mapa)](http://www.openstreetmap.org/search?query=' + urllib.parse.quote(event.get("place")) + ')\n'

          peoplego= 0
          if 'users' in event and len(event['users']) > 0:
              for u in event['users']:
                  if u['go'] == 1:
                       peoplego += u['go']
              if peoplego > 1:
                  message_text += '\n\U0001F465 Hi assistiran *' + str(peoplego) + '* persones.'
              elif peoplego == 1:
                  message_text += '\n\U0001F464 Hi assistirà *una* persona.'
         #    message_text += '\n'
         #    message_text += '\n_Assistents:_ '
         #    for u in event['users']:
         #        message_text += '- ' + u['first_name']
          message_text += '\n\n'

          return message_text

    if 'type' in event and event['type'] == 'Notícia':
          message_text = "*{name}*\n".format(
              name=event['name']
          )

          if 'description' in event:
              message_text += '_' + event['description'] + '_\n'

         #if 'users' in event and len(event['users']) > 0:
         #    message_text += '\nVotació: \n'
         #    for u in event['users']:
         #        message_text += u['first_name']
         #        message_text += str(u['like']) + '\n'

          message_text += '\n'

          return message_text

    if 'type' in event and event['type'] == 'Paquets de llengua':
          f= open(paths['versions']+"android_version.txt","r")
          android_date= f.read(10)
          f.close()
          f= open(paths['versions']+"ios_version.txt","r")
          ios_date= f.read(10)
          f.close()
          f= open(paths['versions']+"tdesktop_version.txt","r")
          tdesktop_date= f.read(10)
          f.close()
          #message_text = "*{name}*\n".format(
          #    name=event['name']
          #)
          if event['android'] != 'NOT' and event['ios'] != 'NOT' and event['tdesktop'] != 'NOT':
                pack= 'els paquets'
                updated_packs= 'les aplicacions d\'Android, iOS i Telegram Desktop'
          elif event['android'] != 'NOT' and event['ios'] != 'NOT' and event['tdesktop'] == 'NOT':
                pack= 'els paquets'
                updated_packs= 'les aplicacions d\'Android i iOS'
                not_pack= 'del paquet'
                not_updated_packs= 'Telegram Desktop (' + tdesk_date + ')'
          elif event['android'] != 'NOT' and event['ios'] == 'NOT' and event['tdesktop'] != 'NOT':
                pack= 'els paquets'
                updated_packs= 'les aplicacions d\'Android i Telegram Desktop'
                not_pack= 'del paquet'
                not_updated_packs= 'iOS (' + ios_date + ')'
          elif event['android'] == 'NOT' and event['ios'] != 'NOT' and event['tdesktop'] != 'NOT':
                pack= 'els paquets'
                updated_packs= 'les aplicacions d\'iOS i Telegram Desktop'
                not_pack= 'del paquet'
                not_updated_packs= 'Android (' + android_date + ')'
          elif event['android'] != 'NOT' and event['ios'] == 'NOT' and event['tdesktop'] == 'NOT':
                pack= 'el paquet'
                updated_packs= 'l\'aplicació d\'Android'
                not_pack= 'dels paquets'
                not_updated_packs= 'iOS (' + ios_date + ') i Telegram Desktop (' + tdesktop_date + ')'
          elif event['android'] == 'NOT' and event['ios'] != 'NOT' and event['tdesktop'] == 'NOT':
                pack= 'el paquet'
                updated_packs= 'l\'aplicació d\'iOS'
                not_pack= 'dels paquets'
                not_updated_packs= 'Android (' + android_date + ') i Telegram Desktop (' + tdesktop_date + ')'
          elif event['android'] == 'NOT' and event['ios'] == 'NOT' and event['tdesktop'] != 'NOT':
                pack= 'el paquet'
                updated_packs= 'l\'aplicació Telegram Desktop'
                not_pack= 'dels paquets'
                not_updated_packs= 'Android (' + android_date + ') i iOS (' + ios_date + ')'
          message_text = '\nBon dia!\n'
          message_text += 'Hem actualitzat ' + pack + ' de llengua del Telegram, amb data del ' + event['date_version'] + ', per a ' + updated_packs + '.\n'
          if event['android'] == 'NOT' or event['ios'] == 'NOT' or event['tdesktop'] == 'NOT':
              message_text += 'També teniu disponible una versió més antiga ' + not_pack + ' de llengua per a ' + not_updated_packs + '.\n\n' 
          if 'description' in event:
              message_text += event['description']

          message_text += '\n'

          return message_text

class InlineModule(object):
    def __init__(self):
        self.handlers = [
            InlineQueryHandler(self.inline_query),
            CallbackQueryHandler(self.callback_handler)
        ]
        self.store = TinyDBStore()

    def callback_handler(self, bot, update):
        query = update.callback_query
        data = query.data
        user = query.from_user.__dict__

        (command, event_id) = tuple(data.split('_'))
        event = self.store.get_event(event_id)

        if not event.get('users'):
            event['users'] = []

        if 'type' in event and event['type'] == 'Notícia':
              if any(u['id'] == user['id'] for u in event['users']):
                    if any(u['id'] == user['id'] and u['like'] == 0 for u in event['users']):
                          user.update({'like': 0})
                    elif any(u['id'] == user['id'] and u['like'] == 1 for u in event['users']):
                          user.update({'like': 1})
                    elif any(u['id'] == user['id'] and u['like'] == 2 for u in event['users']):
                          user.update({'like': 2})

        if 'type' in event and event['type'] == 'Esdeveniment':
              if any(u['id'] == user['id'] for u in event['users']):
                    if any(u['id'] == user['id'] and u['go'] == 1 for u in event['users']):
                          user.update({'go': 1})

        if command == 'go':
            event = self.toggle_user(event, user)

        if command == 'like':
            event = self.toggle_like(event, user)

        if command == 'nolike':
            event = self.toggle_nolike(event, user)

        bot.editMessageText(text=create_event_message(event, user),
                            inline_message_id=query.inline_message_id,
                            reply_markup=InlineKeyboardMarkup(inline_keyboard=create_keyboard(event, user)),
                            parse_mode=ParseMode.MARKDOWN,
			    disable_web_page_preview=True)

    def toggle_user(self, event, user):
        if not event.get('users'):
            event['users'] = []

        if any(u['id'] == user['id'] for u in event['users']):
            event['users'].remove(user)
        else:
            user.update({'go': 1})
            event['users'].append(user)

        self.store.update_event(event)
        return event

    def toggle_like(self, event, user):
        if not event.get('users'):
            event['users'] = []

        if any(u['id'] == user['id'] and u['like'] == 0 for u in event['users']):
               event['users'].remove(user)
               user.update({'like': 1})
               event['users'].append(user)
        elif any(u['id'] == user['id'] and u['like'] == 1 for u in event['users']):
               event['users'].remove(user)
               user.update({'like': 0})
               event['users'].append(user)
        elif any(u['id'] == user['id'] and u['like'] == 2 for u in event['users']):
               event['users'].remove(user)
               user.update({'like': 1})
               event['users'].append(user)
        else:
               user.update({'like': 1})
               event['users'].append(user)

        self.store.update_event(event)
        return event

    def toggle_nolike(self, event, user):
        if not event.get('users'):
            event['users'] = []

        if any(u['id'] == user['id'] and u['like'] == 0 for u in event['users']):
               event['users'].remove(user)
               user.update({'like': 2})
               event['users'].append(user)
        elif any(u['id'] == user['id'] and u['like'] == 1 for u in event['users']):
               event['users'].remove(user)
               user.update({'like': 2})
               event['users'].append(user)
        elif any(u['id'] == user['id'] and u['like'] == 2 for u in event['users']):
               event['users'].remove(user)
               user.update({'like': 0})
               event['users'].append(user)
        else:
               user.update({'like': 2})
               event['users'].append(user)

        self.store.update_event(event)
        return event

    def inline_query(self, bot, update):
        query = update.inline_query.query
        user_id = update.inline_query.from_user.id
        user = update.inline_query.from_user.__dict__

        if str(user_id) in allowed_users.values():
          with open(paths['inline']+'inline_status.csv', 'rt') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
              for field in row:
                if field == str(user_id) + '_admin':
                  results = []
                  events = self.store.get_events(user_id, query)

                  for event in events:
                      keyboard = create_keyboard(event, user)
                      result = InlineQueryResultArticle(id=event.eid,
                                                        title=event['name'],
                                                        description=event['description'],
                                                        thumb_url='https://gent.softcatala.org/albert/softcatalabot/softcatalabot_calendar.png',
                                                        input_message_content=InputTextMessageContent(
                                                            create_event_message(event, user),
                                                            parse_mode=ParseMode.MARKDOWN,
						            disable_web_page_preview=True
                                                        ),
                                                        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))
                      results.append(result)

                  bot.answerInlineQuery(
                      update.inline_query.id,
                      results=results,
                      cache_time=30,
                      switch_pm_text='Canvia l\'estatus de l\'inline a normal',
                      switch_pm_parameter='change-inline-status',
                      is_personal=True
                  )

        #elif str(user_id) in allowed_users.values() and inline_status[str(user_id)] == 'normal':
                elif field == str(user_id) + '_normal':
                  results = []
                  packs = self.store.get_packs(query)

                  for pack in packs: 

                      result = InlineQueryResultCachedDocument(id=pack.eid,
                                                               title=pack['name'],
                                                               document_file_id=pack['cached_id'],
                                                               description=pack['description'],
                                                               caption=pack['howto']
                                                               )
                      results.append(result)

                  bot.answerInlineQuery(
                      update.inline_query.id,
                      results=results,
                      cache_time=30,
                      switch_pm_text='Canvia l\'estatus de l\'inline a administrador',
                      switch_pm_parameter='change-inline-status',
                      is_personal=True
                  )

    def get_handlers(self):
        return self.handlers

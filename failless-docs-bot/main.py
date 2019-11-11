#!/usr/bin/env python

############################################
# File Name : main.py
# Purpose : just for fun
# Creation Date : 30-10-2019
# Last Modified : Чт 31 окт 2019 00:07:08
# Created By : Andrey Prokopenko, BMSTU
############################################

import re
import os
import requests
import logging
from io import BytesIO
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from PIL import Image


TOKEN = os.getenv('TG_BOT_TOKEN')
CHAT_ID = '-1001496566345'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please send msg")

def publish_link(update, context):
    print(update.effective_chat.id)
    if update.message is not None:
        if 'http' in update.message.text:
            context.bot.send_message(chat_id=CHAT_ID, text=update.message.text)
        return
    context.bot.send_message(chat_id=update.effective_chat.id, text='Pandas is love <3')


def publish_docs(update, context):
    print(update.message)
    newFile = context.bot.get_file(update.message.photo[0]['file_id'])
    newFile.download('files/image{}.jpeg'.format(update.message.message_id))
    bio = BytesIO()
    bio.name = 'files/image{}.jpeg'.format(update.message.message_id)
    image = Image.open(bio.name)
    image.save(bio, 'JPEG')
    bio.seek(0)
    context.bot.send_photo(chat_id=CHAT_ID, photo=bio)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    echo_handler = MessageHandler(Filters.text, publish_link)
    dp.add_handler(echo_handler)
    dp.add_handler(MessageHandler(Filters.photo, publish_docs))
    #dp.add_handler(MessageHandler(Filters.document, publish_docs))
    unknown_handler = MessageHandler(Filters.command, unknown)
    dp.add_handler(unknown_handler)
    updater.start_polling()
    #updater.idle()

if __name__ == '__main__':
    main()

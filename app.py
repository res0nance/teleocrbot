import telepot
import pprint
import telepot.loop
import os
import time
from PIL import Image, features
import tesserocr

telegram_botid = 'TELEGRAM_BOTID'

bot = telepot.Bot(telegram_botid)
path = os.path.dirname(__file__)

def handle(msg):
    pprint.pprint(msg)
    if( 'sticker' in msg ):
        filename = 'temp.webp'
        bot.download_file(msg['sticker']['file_id'], os.path.join(path,filename))
        img = Image.open(filename)
        text = tesserocr.image_to_text(img)
        text = text.strip()
        pprint.pprint(text)
        if text:
            bot.sendMessage(msg['chat']['id'], text)
    if( 'document' in msg ):
        filename = ''
        if( msg['document']['mime_type'] == 'image/jpeg'):
            filename = 'temp.jpg'
        if( msg['document']['mime_type'] == 'image/png'):
            filename = 'temp.png'
        if filename:
            bot.download_file(msg['document']['file_id'], os.path.join(path,filename))
            img = Image.open(filename)
            text = tesserocr.image_to_text(img)
            text = text.strip()
            pprint.pprint(text)
            if text:
                bot.sendMessage(msg['chat']['id'], text)
    if( 'photo' in  msg ):
        filename = 'temp.jpg'
        bot.donwload_file(msg['photo'][-1]['file_id'], os.path.join(path,filename))
        img = Image.open(filename)
        text = tesserocr.image_to_text(img)
        text = text.strip()
        pprint.pprint(text)
        if text:
            bot.sendMessage(msg['chat']['id'], text)


pprint.pprint(tesserocr.get_languages())
pprint.pprint(bot.getMe())
telepot.loop.MessageLoop(bot,handle).run_as_thread()

while 1:
    time.sleep(10)

import telepot
import pprint
import telepot.loop
import os
import time
from PIL import Image, features
import tesserocr

telegram_botid = 'TELEGRAM_BOTID'

bot = telepot.Bot(telegram_botid)

def handle(msg):
    pprint.pprint(msg)
    if( 'sticker' in msg ):
        path = os.path.dirname(__file__)
        filename = 'temp.webp'
        bot.download_file(msg['sticker']['file_id'], os.path.join(path,filename))
        img = Image.open('temp.webp')
        text = tesserocr.image_to_text(img)
        text = text.strip()
        if text:
            bot.sendMessage(msg['chat']['id'], text)

pprint.pprint(tesserocr.get_languages())
pprint.pprint(bot.getMe())
telepot.loop.MessageLoop(bot,handle).run_as_thread()

while 1:
    time.sleep(10)

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
supported_lang = ""
languages = []

def sendReply(msg,text):
    bot.sendMessage(msg['chat']['id'], text, reply_to_message_id = msg['message_id'])

def runOCR(filename,lang):
    img = Image.open(filename)
    text = tesserocr.image_to_text(img, lang=lang)
    text = text.strip()
    pprint.pprint(text)
    return text

def processOCR(msg, lang):
    if( 'sticker' in msg ):
        filename = 'temp.webp'
        bot.download_file(msg['sticker']['file_id'], os.path.join(path,filename))
        text = runOCR(filename,lang)
        if text:
            sendReply(msg,text)
    if( 'document' in msg ):
        filename = ''
        if( msg['document']['mime_type'] == 'image/jpeg'):
            filename = 'temp.jpg'
        if( msg['document']['mime_type'] == 'image/png'):
            filename = 'temp.png'
        if filename:
            bot.download_file(msg['document']['file_id'], os.path.join(path,filename))
            text = runOCR(filename,lang)
            if text:
                sendReply(msg,text)
    if( 'photo' in  msg ):
        filename = 'temp.jpg'
        bot.download_file(msg['photo'][-1]['file_id'], os.path.join(path,filename))
        text = runOCR(filename, lang)
        if text:
            bot.sendMessage(msg['chat']['id'], text, reply_to_message_id = msg['message_id'])

def handle(msg):
    pprint.pprint(msg)
    commandtext = msg['text']
    commandtext = command.strip()
    if not commandtext:
        return
    commands = commands.split()
    arglen = len(commands)
    if arglen == 1 and command[0] == '/lang':
        bot.sendMessage(msg['chat']['id'], supported_lang, reply_to_message_id = msg['message_id'])
    if arglen == 2 and command[0] == '/OCR' and command[1] in languages:
        if 'reply_to_message' in msg:
            processOCR(msg['reply_to_message'], command[1])

language = tesserocr.get_languages()
for lang in language:
    if lang != 'osd' and lang != 'equ':
        languages.append(lang)

supported_lang = ','.join(languages)

pprint.pprint(bot.getMe())
telepot.loop.MessageLoop(bot,handle).run_as_thread()

while 1:
    time.sleep(10)

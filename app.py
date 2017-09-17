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
failedOCR = "Could not recognize any characters sorry :("

def sendReply(msg,text):
    bot.sendMessage(msg['chat']['id'], text, reply_to_message_id = msg['message_id'])

def runOCR(filename,lang):
    img = Image.open(filename)
    pprint.pprint('Start OCR on image with language set ' + lang)
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
        else:
            sendReply(msg,failedOCR)
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
            else:
                sendReply(msg,failedOCR)
    if( 'photo' in  msg ):
        filename = 'temp.jpg'
        bot.download_file(msg['photo'][-1]['file_id'], os.path.join(path,filename))
        text = runOCR(filename, lang)
        if text:
            sendReply(msg,text)
        else:
            sendReply(msg,failedOCR)

def handle(msg):
    pprint.pprint(msg)
    commandtext = msg['text']
    commandtext = command.strip()
    if not commandtext:
        return
    commands = commandtext.split()
    arglen = len(commands)
    if arglen == 1 and commands[0] == '/lang':
        bot.sendMessage(msg['chat']['id'], supported_lang, reply_to_message_id = msg['message_id'])
    if arglen == 2 and commands[0] == '/ocr':
        if commands[1] not in languages:
            sendReply(msg,"Unsupported language specified")
            return
        if 'reply_to_message' in msg:
            processOCR(msg['reply_to_message'], commands[1])
        else:
            sendReply(msg, "Must be used in reply to a picture based message")

language = tesserocr.get_languages()
for lang in language[1]:
    if lang != 'osd' and lang != 'equ':
        languages.append(lang)

supported_lang = ','.join(languages)

pprint.pprint(bot.getMe())
telepot.loop.MessageLoop(bot,handle).run_as_thread()

while 1:
    time.sleep(10)

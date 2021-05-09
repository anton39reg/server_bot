import logging
import sys

from queue import Queue
from threading import Thread
from waitress import serve
from flask import Flask, request

from telegram import Bot, Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, CallbackContext
from telegram.ext import Dispatcher, MessageHandler, Filters

from settings import TOKEN

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger('server')

bot = Bot(TOKEN)
update_queue = Queue()
dispatcher = Dispatcher(bot, update_queue)
thread = Thread(target=dispatcher.start, name='dispatcher')

app = Flask('echo')

chat_to_photos = {}

def start(update: Update, _: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

def help_command(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('Help!')

def echo_text(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(update.message.text)

def echo_photo(update: Update, _: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Yes!", callback_data='1')],
        [InlineKeyboardButton("No!", callback_data='2')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    chat_to_photos[update.message.chat.id] = {'photo':update.message.photo[-1].file_id, 
                                              'send':False}
    update.message.reply_text('Do you want to back photo?', reply_markup=reply_markup)

def button(update: Update, _: CallbackContext) -> None:
    query = update.callback_query

    query.answer()

    if query.data == '1' and chat_to_photos[query.message.chat.id]['send'] is False:
        query.message.reply_text('Get it!')
        query.message.reply_photo(chat_to_photos[query.message.chat.id]['photo'])
    elif query.data == '2' and chat_to_photos[query.message.chat.id]['send'] is False:
        query.message.reply_text('As you know.')
    
    chat_to_photos[query.message.chat.id]['send'] = True

def wrong_data(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('Sorry, we work only with photo or text')

@app.route(f'/{TOKEN}', methods=['POST'])
def echo():
    logger.info(request.get_json())
    update = Update.de_json(request.json, bot)
    update_queue.put(update)
    return {'ok':True}

def set_handlers():
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(CallbackQueryHandler(button))

    dispatcher.add_handler(MessageHandler(Filters.text, echo_text))
    dispatcher.add_handler(MessageHandler(Filters.photo, echo_photo))
    dispatcher.add_handler(MessageHandler(~(Filters.photo | Filters.text), wrong_data))

if __name__ == '__main__':
    set_handlers()

    thread.start()

    bot.setWebhook(f'{sys.argv[1]}/{TOKEN}')
    serve(app, host='0.0.0.0', port='1234')

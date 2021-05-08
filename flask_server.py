import logging
import sys
import requests
from waitress import serve
from flask import Flask, jsonify, request
from settings import TOKEN
from telegram import Bot, Update, ForceReply
from telegram.ext import Dispatcher, Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger('server')

bot = Bot(TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)
app = Flask('echo')

def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo_text(update: Update, _: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def echo_photo(update: Update, _: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_photo(update.message.photo[-1].file_id)

@app.route(f'/{TOKEN}', methods=['POST'])
def echo():
    logger.info(request.get_json())
    update = Update.de_json(request.json, bot)
    dispatcher.process_update(update)
    return {'ok':True}

def set_handlers():
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(Filters.text, echo_text))    
    dispatcher.add_handler(MessageHandler(Filters.photo, echo_photo))    

if __name__ == '__main__':
    set_handlers()
    bot.setWebhook(f'{sys.argv[1]}/{TOKEN}')
    serve(app, host='0.0.0.0', port='5000')

import logging
import sys
import json
import requests

from settings import TOKEN
from telegram import Update, ForceReply
from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger('telebot')

def main(external_url) -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Start the Bot
    # updater.start_polling()
    updater.start_webhook(listen='0.0.0.0', 
                          port=1234,
                          url_path=TOKEN,
                          webhook_url=f'{external_url}/{TOKEN}')
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main(sys.argv[1])

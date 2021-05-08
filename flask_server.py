import logging
import requests
from waitress import serve
from flask import Flask, jsonify, request
from settings import TOKEN

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger('server')

app = Flask('echo')

def send_message(chat_id, text):
    method = "sendMessage"
    url = f"https://api.telegram.org/bot{TOKEN}/{method}"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)


@app.route(f'/{TOKEN}', methods=['POST'])
def echo():
    logger.info(request.get_json())
    chat_id = request.json['message']['chat']['id']
    send_message(chat_id, request.json['message']['text'])
    return {'ok':True}   

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port='5000')

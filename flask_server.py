import logging
from waitress import serve
from flask import Flask, jsonify, request
from settings import TOKEN

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger('server')

app = Flask('echo')

@app.route(f'/{TOKEN}', methods=['POST'])
def echo():
    logger.info(request.get_json())
    return jsonify(
        {
            "data": request.data.decode("utf-8"),
            "form": request.form,
            "json": request.get_json(),
        }
    )
   
if __name__ == '__main__':
    serve(app, host='0.0.0.0', port='5000')

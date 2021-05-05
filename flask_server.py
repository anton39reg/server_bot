from waitress import serve
from flask import Flask, jsonify, request
from settings import TOKEN

app = Flask('echo')

@app.route(f'/{TOKEN}', methods=['POST'])
def echo():
    return jsonify(
        {
            "data": request.data.decode("utf-8"),
            "form": request.form,
            "json": request.get_json(),
        }
    )
   
if __name__ == '__main__':
    serve(app, host='0.0.0.0', port='5000')

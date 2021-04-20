__author__ = 'thaiph99'

from flask import Flask, json, Response, request, render_template
from werkzeug.utils import secure_filename
from os import path, getcwd
from collections import Counter
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def success_handle(output, status=200, mimetype='application/json'):
    return Response(output, status=status, mimetype=mimetype)


def error_handle(error_message, status=500, mimetype='application/json'):
    return Response(json.dumps({"error": {"message": error_message}}), status=status, mimetype=mimetype)


@app.route('/', methods=['GET'])
def home():
    output = json.dumps({"api": '1.0'})
    return success_handle(output)


def process(list_urls, list_keys):
    pass


@app.route('/action', methos=['POST'])
def action():
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='3000')

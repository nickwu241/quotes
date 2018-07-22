#!/usr/bin/env python
import json
import os

from flask import Flask, jsonify
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

with open('quotes.json') as f:
    QUOTES = json.load(f)

@app.route('/')
def index():
    return 'Hello! GET /quotes for a list of quotes :)'

@app.route('/quotes')
def quotes():
    return jsonify(QUOTES)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

#!/usr/bin/env python
import json
import random
import os

from flask import abort, Flask, jsonify
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

@app.route('/quotes/random')
def quotes_random():
    return jsonify(random.choice(QUOTES))

@app.route('/quotes/<int:quote_id>')
def quotes_id(quote_id):
    if quote_id >= len(QUOTES):
        abort(404)
    return jsonify(QUOTES[quote_id])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

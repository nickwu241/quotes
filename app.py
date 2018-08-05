#!/usr/bin/env python
import json
import math
import os
import random

from flask import Flask, abort, jsonify, send_from_directory

app = Flask(__name__, static_url_path='')
app.config['JSON_AS_ASCII'] = False

with open('quotes/all.json') as f:
    QUOTES = json.load(f)

ENTRIES_PER_PAGE = 100
LAST_PAGE = math.ceil(len(QUOTES) / ENTRIES_PER_PAGE)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/endpoints')
def endpoints():
    return jsonify([str(r) for r in app.url_map.iter_rules()
                    if str(r).startswith('/quotes')])

@app.route('/quotes/discover_paths')
def quotes_discover_paths():
    quote_paths = [f for f in os.listdir('quotes') if f.endswith('.json')]
    return jsonify(quote_paths)

@app.route('/quotes/random')
def quotes_random():
    return jsonify(random.choice(QUOTES))

@app.route('/quotes/', defaults={'page': 1})
@app.route('/quotes/page/<int:page>')
def quotes_page(page):
    if page > LAST_PAGE:
        abort(404)
    start = (page-1) * ENTRIES_PER_PAGE
    end = min(start+ENTRIES_PER_PAGE, len(QUOTES))
    return jsonify(QUOTES[start:end])

@app.route('/quotes/<int:quote_id>')
def quotes_id(quote_id):
    if quote_id >= len(QUOTES):
        abort(404)
    return jsonify(QUOTES[quote_id])

@app.route('/quotes/<path:json_path>')
def quotes_path(json_path):
    return send_from_directory('quotes', json_path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

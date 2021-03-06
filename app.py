#!/usr/bin/env python
import math
import os

from flask import Flask, abort, jsonify, request, send_from_directory

import messenger
import quotes

app = Flask(__name__, static_url_path='')
app.config['JSON_AS_ASCII'] = False

QUOTES = quotes.get_all_quotes()
ENTRIES_PER_PAGE = 100
LAST_PAGE = math.ceil(len(QUOTES) / ENTRIES_PER_PAGE)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/privacy_policy')
def privacy_policy():
    return send_from_directory('static', 'privacy_policy.html')

@app.route('/messenger_webhook', methods=['GET', 'POST'])
def messenger_webhook():
    return messenger.handle_request(request)

@app.route('/metadata')
def metadata():
    return jsonify(METADATA)

@app.route('/quotes/random')
def quotes_random():
    return jsonify(quotes.random_quote())

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
    if quote_id > len(QUOTES):
        abort(404)
    return jsonify(QUOTES[quote_id-1])

@app.route('/quotes/paths')
def quotes_paths():
    return jsonify(METADATA['paths'])

@app.route('/quotes/paths/<path:json_path>')
def quotes_path(json_path):
    return send_from_directory('quotes', json_path)

METADATA = {
    'number_of_quotes': len(QUOTES),
    'pages': LAST_PAGE,
    'paths': [f for f in os.listdir('quotes') if f.endswith('.json')],
    'endpoints' : [str(r) for r in app.url_map.iter_rules()
                   if str(r).startswith('/quotes')],
}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

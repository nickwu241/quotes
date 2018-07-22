#!/usr/bin/env python
import json

from bs4 import BeautifulSoup
import requests

URL = 'http://www.keepinspiring.me/famous-quotes'

html = requests.get(URL).text
soup = BeautifulSoup(html, 'html.parser')

quotes_json = []
quotes_div = soup.find_all('div', class_='author-quotes')
for q in quotes_div:
    if not q.contents or not q.contents[0].strip():
        continue
    quote = q.contents[0].strip(' “”')
    author_span = q.find('span', class_='quote-author-name')
    author = author_span.text.strip(' -') if author_span else 'Unknown'
    quotes_json.append({'quote': quote, 'author': author})

with open('quotes.json', 'w', encoding='utf8') as f:
    json.dump(quotes_json, f, ensure_ascii=False)

#!/usr/bin/env python
import json
import os
from multiprocessing import Pool
from time import sleep

import requests
from bs4 import BeautifulSoup


def get_quotes_list_from_html(content):
    soup = BeautifulSoup(content, 'html.parser')
    quotes_list = []
    quote_divs = soup.find_all('div', class_='author-quotes')
    for div in quote_divs:
        div_text = div.text.strip()
        if not div_text:
            continue

        author = 'Unknown'
        parts = div_text.split('”')
        if len(parts) == 1:
            quote = parts[0]
        elif len(parts) == 2:
            quote, author = parts
        else:
            i = div_text.rfind('”')
            quote, author = div_text[:i], div_text[i:]

        quote = quote.lstrip(' 1234567890.').strip(' “”')
        author = author.split('\n', 2)[0].strip(' –—―-') or 'Unknown'
        quotes_list.append({'quote': quote, 'author': author})
    return quotes_list


def __extract_quotes_to_disk(link, name, overwrite=False):
    print(f'__extract_quotes_to_disk({link}, {name}, overwrite={overwrite})')

    filename = os.path.join('quotes', f'{name}.json')
    if not overwrite and os.path.isfile(filename):
        return f'Skipped {link}: {filename} already exists'

    resp = requests.get(link)
    resp.raise_for_status()
    sleep(2)
    try:
        quotes_list = get_quotes_list_from_html(resp.text)
    except ValueError as e:
        return f'Failed parsing content from {link}: {e}'

    print(f'Writing to contents of {link} to {filename}...')
    with open(filename, 'w', encoding='utf8') as f:
        json.dump(quotes_list, f, ensure_ascii=False)
    return None


def main():
    args = []
    for i in range(1, 5):
        with open(f'category-quotes-{i}.html') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        for title_h2 in soup.find_all('h2', class_='entry-title'):
            article_link = title_h2.find('a')['href']
            article_name = article_link.strip('/').split('/')[-1]
            args.append((article_link, article_name, True))

    with Pool(10) as pool:
        errors = [e for e in pool.starmap(__extract_quotes_to_disk, args) if e]
    for e in errors:
        print(e)

if __name__ == '__main__':
    main()

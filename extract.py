#!/usr/bin/env python
import json
import os
from time import sleep

import requests
from bs4 import BeautifulSoup


class ExtractionError(Exception):
    pass


def get_quotes_list_from_html(content):
    soup = BeautifulSoup(content, 'html.parser')
    quotes_list = []
    quote_divs = soup.find_all('div', class_='author-quotes')
    for div in quote_divs:
        if not div.text.strip():
            continue
        quote, author = div.text.strip().split('”')
        quote = quote.strip(' “”')
        author = author.split('\n', 2)[0].strip(' –—―-') or 'Unknown'
        quotes_list.append({'quote': quote, 'author': author})
    return quotes_list


def __extract_quotes_to_disk(link, name, overwrite=False):
    print(f'__extract_quotes_to_disk({link}, {name}, overwrite={overwrite})')

    filename = os.path.join('quotes', f'{name}.json')
    if not overwrite and os.path.isfile(filename):
        print(f'Skipped {link}: {filename} already exists')
        return

    resp = requests.get(link)
    resp.raise_for_status()
    sleep(2)
    try:
        quotes_list = get_quotes_list_from_html(resp.text)
    except ValueError as e:
        raise ExtractionError(f'Failed parsing content from {link}: {e}')

    print(f'Writing to contents of {link} to {filename}...')
    with open(filename, 'w', encoding='utf8') as f:
        json.dump(quotes_list, f, ensure_ascii=False)


def main():
    article_names_to_links = {}
    for i in range(1, 5):
        with open(f'category-quotes-{i}.html') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        for title_h2 in soup.find_all('h2', class_='entry-title'):
            article_link = title_h2.find('a')['href']
            article_name = article_link.strip('/').split('/')[-1]
            article_names_to_links[article_name] = article_link

    failed_links_to_errors = {}
    for name, link in article_names_to_links.items():
        try:
            __extract_quotes_to_disk(link, name, overwrite=True)
        except ExtractionError as e:
            failed_links_to_errors[link] = e

    for link, err in failed_links_to_errors.items():
        print(f'Error exctracting {link}: {err}')


if __name__ == '__main__':
    main()

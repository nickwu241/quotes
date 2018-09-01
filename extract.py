#!/usr/bin/env python
import json
import multiprocessing
import os

import requests
from bs4 import BeautifulSoup

CACHE_DIR = 'scrape-cache'

def get_quotes_list_from_html(content):
    soup = BeautifulSoup(content, 'html.parser')
    for script in soup('script'):
        script.extract()

    quotes_list = []
    for div in soup('div', class_='author-quotes'):
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

def __parse_quote_page_to_disk(quote_page_filepath):
    with open(quote_page_filepath) as f:
        html = f.read()
    output_filename = os.path.basename(quote_page_filepath) + '.json'
    output_filepath = os.path.join('quotes', output_filename)
    print(f'Parsing contents of {quote_page_filepath} to {output_filepath}')
    with open(output_filepath, 'w', encoding='utf8') as f:
        json.dump(get_quotes_list_from_html(html), f, ensure_ascii=False)

def __download_quote_page(url, should_overwrite_cache=False):
    filename = url.strip('/').split('/')[-1]
    filepath = os.path.join(CACHE_DIR, filename)
    if not should_overwrite_cache and os.path.isfile(filepath):
        print(f'Skipping {url} because {filepath} already exists')
        return filepath

    print(f'Downloading {url} to {filepath}...')
    resp = requests.get(url)
    resp.raise_for_status()
    with open(filepath, 'w') as f:
        f.write(resp.text)
    return filepath

def __get_urls_from_category_quotes():
    urls = []
    for i in range(1, 5):
        with open(f'category-quotes-{i}.html') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        for title_h2 in soup.find_all('h2', class_='entry-title'):
            urls.append(title_h2.find('a')['href'])
    return urls

def __mkdir_cache_dir():
    os.makedirs(CACHE_DIR, exist_ok=True)

def main():
    do_overwrite_cache = False
    __mkdir_cache_dir()
    args = [(url, do_overwrite_cache) for url in __get_urls_from_category_quotes()]
    with multiprocessing.Pool() as pool:
        filepaths = pool.starmap(__download_quote_page, args)
        pool.map(__parse_quote_page_to_disk, filepaths)

if __name__ == '__main__':
    main()

#!/usr/bin/env python
import re
from time import sleep

import requests
from bs4 import BeautifulSoup

__PAGE_PATTERN = re.compile(r'/category/quotes/page/(\d+)/$')


def download_quote_pages():
    next_link = 'http://www.keepinspiring.me/category/quotes/'
    while True:
        resp = requests.get(next_link)
        resp.raise_for_status()
        __write_to_file(contents=resp.text, link=next_link)
        soup = BeautifulSoup(resp.text, 'html.parser')
        try:
            next_link = soup.select('li.next.right')[0].find('a')['href']
        except TypeError:
            return
        sleep(1)


def __write_to_file(contents, link):
    match = __PAGE_PATTERN.search(link)
    page_number = match.group(1) if match else '1'
    filename = f'category-quotes-{page_number}.html'

    print(f'Writing to contents of {link} to {filename}...')
    with open(filename, 'w') as f:
        f.write(contents)


if __name__ == '__main__':
    download_quote_pages()

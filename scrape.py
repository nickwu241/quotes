#!/usr/bin/env python
from download import download_quote_pages
import extract

if __name__ == '__main__':
    download_quote_pages()
    extract.main()

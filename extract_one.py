#!/usr/bin/env python
import sys

from extract import get_quotes_list_from_html

with open(sys.argv[1]) as f:
    print(get_quotes_list_from_html(f.read()))

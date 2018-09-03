import json
import random

with open('quotes/all.json') as f:
    __QUOTES = json.load(f)

def get_all_quotes():
    return __QUOTES

def random_quote():
    return random.choice(__QUOTES)

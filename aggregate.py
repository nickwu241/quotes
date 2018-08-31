#!/usr/bin/env python
import json
import os

ALL_JSON_FILEPATH = os.path.join('quotes', 'all.json')

def __clean_aggregate(quotes):
    return [q for q in quotes if 'eval(' not in q['quote']]

def __get_aggregate():
    all_quotes = []
    for filename in os.listdir('quotes'):
        if not filename.endswith('.json') or filename == 'all.json':
            continue

        filepath = os.path.join('quotes', filename)
        print(f'Appending {filepath}...')
        quotes_list = __read_json(filepath)
        for item in quotes_list:
            item['tag'] = filename[:-5]
        all_quotes += quotes_list
    return all_quotes

def __write(quotes):
    with open(ALL_JSON_FILEPATH, 'w', encoding='utf8') as f:
        json.dump(quotes, f, ensure_ascii=False)

def __read_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def main():
    __write(__clean_aggregate(__get_aggregate()))
    print(f'Wrote aggregation to {ALL_JSON_FILEPATH}')

if __name__ == '__main__':
    main()

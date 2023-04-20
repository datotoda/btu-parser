import json
import os
from os.path import exists

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from log import now

load_dotenv()

DB_JSON = 'parser_db.json'
KEY_LAST_FILENAME = 'last_json_filename'
KEY_FILENAME_PREFIX = 'file_prefix'

URL = 'https://classroom.btu.edu.ge/ge/student/me/courses'
MESSAGES_URL = 'https://classroom.btu.edu.ge/ge/messages/index/0/1000'
COOKIE = os.environ['cookie']


def to_num(text):
    if '.' not in text or text.split('.')[-1].strip('0') == '':
        return int(text.split('.')[0])
    return round(float(text), 2)


def _get_soup(result_html):
    return BeautifulSoup(result_html, 'html.parser')


def _get_grid(soup):
    table = soup.find('table')
    tag_grid = [list(r)[1::2] for r in table.find_all('tr')[:7]]
    grid = list(map(lambda tag_row: list(map(lambda x: x.text.strip(), tag_row))[1:], tag_grid))
    return grid


def get_grid(result_html):
    return _get_grid(_get_soup(result_html))


def grid_json(result_html):
    grid = get_grid(result_html)
    return {
        'headers': grid[0][1:3],
        'keys': [val[1] for val in grid[1:]],
        'grades': {val[1]: to_num(val[2]) for val in grid[1:]}
    }


def get_db_json():
    with open(DB_JSON, 'r') as file:
        return json.load(file)


def set_db_json(key, value):
    j = get_db_json()
    j[key] = value
    with open(DB_JSON, 'w') as file:
        json.dump(j, file, indent=4)


def get_filename(datetime):
    return datetime.strftime(f'{ get_db_json()[KEY_FILENAME_PREFIX] }/%y_%m_%d.json')


def get_today_filename():
    return get_filename(now())


def get_json_from_history(filename):
    result_json = {}
    if exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            result_json = json.load(file)
    return result_json


def save_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def get_html_text(html):
    return html.text


def get_response(messages=False):
    url = URL
    if messages:
        url = MESSAGES_URL
    return requests.get(url, headers={'cookie': COOKIE})


def response_api(html_text):
    new_json = grid_json(html_text)
    old_json = get_json_from_history(get_db_json()[KEY_LAST_FILENAME])

    if old_json == new_json:
        return {}

    new_filename = get_today_filename()
    save_json(new_json, new_filename)
    set_db_json(KEY_LAST_FILENAME, new_filename)

    new_json['deltas'] = {key: 0 for key in new_json['keys']}

    if old_json and old_json['grades'].keys() == new_json['grades'].keys():
        for key in new_json['keys']:
            new_json['deltas'][key] = to_num(str(new_json['grades'][key] - old_json['grades'][key]))

    return new_json


def get_has_messages(result_html):
    soup = _get_soup(result_html)
    messages_count  = int(soup.find_all('a', attrs={'href': 'https://classroom.btu.edu.ge/ge/messages'})[0].text.strip())
    has_messages = messages_count > 0
    return has_messages
    

def get_message_urls(result_html):
    urls = _get_soup(result_html).find_all('tr', attrs={'class': 'info'})
    urls = list(map(lambda tr: tr.find('a').attrs['href'], urls))
    return urls


def get_messages(result_html):
    messages = []
    message_urls = get_message_urls(result_html)
    for url in message_urls:
        html_text = get_html_text(get_response(url=url))
        soup = _get_soup(html_text)
        title = ' '.join(soup.find('legend').text.replace('\n\n', '-').split())
        message_text = soup.find(id='message_body').text
        messages.append({
            'title': title,
            'message_text': message_text,
            'url': url
        })
    return messages

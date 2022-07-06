from datetime import datetime
from os.path import exists

import pytz


LOG_FOLDER = 'log'

ZONE = pytz.timezone('Asia/Tbilisi')


def now():
    return datetime.now(ZONE)


def _log_time_format(t):
    return t.strftime("%m/%d/%Y, %H:%M:%S")


def _get_filename(t):
    return t.strftime("%W week of %Y")


def _get_file_path(filename):
    return f'{LOG_FOLDER}/{filename}.log'


def get_log_time():
    return _log_time_format(now())


def get_file_path():
    return _get_file_path(_get_filename(now()))


def log(message):
    with open(get_file_path(), 'a') as f:
        f.write(f'[{get_log_time()}] {message}\n')


def get_last_log():
    file_path = get_file_path()
    if exists(file_path):
        with open(file_path, 'r') as f:
            return f.read().replace('\n', '<br>')
    return ''

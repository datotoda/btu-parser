from datetime import datetime
from os.path import exists
from firebase import update_to_log, get_from_key

import pytz


ZONE = pytz.timezone('Asia/Tbilisi')


def now():
    return datetime.now(ZONE)


def _log_time_format(t):
    return t.strftime("%m/%d/%Y, %H:%M:%S")


def get_log_time():
    return _log_time_format(now())


def get_new_log_key():
    return datetime.timestamp(now())


def log(message):
    update_to_log(key=get_new_log_key(), value=f'[{get_log_time()}] {message}\n')


def get_last_log():
    logs = get_from_key('log')
    if logs:
        logs = sorted(logs.items(), lambda x: x[0])
        logs = [i[1] for i in logs][-50:]
        return '<br>'.join(logs)
    return ''

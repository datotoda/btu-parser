import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime
import pytz

from dotenv import load_dotenv

load_dotenv()

project_id = os.environ['project_id']
private_key_id = os.environ['private_key_id']
private_key = os.environ['private_key']
client_email = os.environ['client_email']
client_id = os.environ['client_id']
client_x509_cert_url = os.environ['client_x509_cert_url']
databaseURL = os.environ['databaseURL']

cred = credentials.Certificate({
    "project_id": project_id,
    "private_key_id": private_key_id,
    "private_key": private_key,
    "client_email": client_email,
    "client_id": client_id,
    "client_x509_cert_url": client_x509_cert_url,

    "type": "service_account",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "universe_domain": "googleapis.com"
})

firebase_admin.initialize_app(cred, {
    'databaseURL': databaseURL
})

REF = db.reference('py/')

def update_to_key(key, value):
    REF.update({key: value})

def get_from_key(key):
    result = REF.get()
    if result:
        result = REF.get().get(key, None)
    return result

def update_to_history(key, value):
    history = REF.child('history')
    history.update({key: value})

def get_from_history(key):
    history = REF.child('history')
    result = history.get()
    if result:
        result = result.get(key, None)
    return result

def update_to_log(key, value):
    log = REF.child('log')
    log.update({key: value})

def get_from_log(key):
    log = REF.child('log')
    result = log.get()
    if result:
        result = result.get(key, None)
    return result

def update_to_parser_db(key, value):
    parser_db = REF.child('parser_db')
    parser_db.update({key: value})

def get_from_parser_db(key):
    parser_db = REF.child('parser_db')
    result = parser_db.get()
    if result:
        result = result.get(key, None)
    return result


def init():
    now = datetime.now(pytz.timezone('Asia/Tbilisi'))
    update_to_history(key='initial', value={})
    update_to_log(key=f'{int(datetime.timestamp(now))}', value=f'[{now.strftime("%m/%d/%Y, %H:%M:%S")}] start server (firebase_admin init)')
    if not get_from_parser_db(key='last_json_key'):
        update_to_parser_db(key='last_json_key', value='initial')
    update_to_key(key='pause', value='not paused')

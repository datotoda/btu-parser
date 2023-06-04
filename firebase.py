import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime

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


def update_to_history(key, value):
    history = REF.child('history')
    history.update({key: value})

def get_from_history(key):
    history = REF.child('history')
    return history.get().get(key, None)

def update_to_log(key, value):
    history = REF.child('log')
    history.update({key: value})

def get_from_log(key):
    history = REF.child('log')
    return history.get().get(key, None)

def update_to_parser_db(key, value):
    history = REF.child('parser_db')
    history.update({key: value})

def get_from_parser_db(key):
    history = REF.child('parser_db')
    return history.get().get(key, None)

def update_to_key(key, value):
    REF.update({key: value})

def get_from_key(key):
    return REF.get().get(key, None)


def init():
    update_to_history(key='initial', value={})
    update_to_log(key=f'{int(datetime.timestamp(datetime.now()))}', value='start server (firebase_admin init)')
    update_to_parser_db(key='last_json_key', value='initial')
    update_to_key(key='pause', value='not paused')

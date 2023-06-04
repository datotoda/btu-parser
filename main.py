import os

from dotenv import load_dotenv
from flask import Flask

from log import log, get_last_log
from mailsender import send_email, send_wrong_cookie_email, send_message_email
from html_parser import response_api, get_html_text, get_response, get_has_messages, get_messages
from firebase import init, get_from_key, update_to_key

load_dotenv()

app = Flask('')
app.config['JSON_AS_ASCII'] = False
app.secret_key = os.environ['flask_key']


@app.route('/')
def home():
    return get_last_log()


@app.route('/check')
def check():
    PAUSE = get_from_key(key='pause') == 'paused'
        
    if PAUSE:
        log("Suspended")
        return 'Suspended'
        
    response = {}
    messages = []
    html_text = get_html_text(get_response())
    if html_text:
        if 'ავტორიზაცია' in html_text:
            send_wrong_cookie_email()
            log("wrong cookie")
            return 'wrong cookie'
        try:
            response = response_api(html_text)
        except Exception:
            return {}
        
        try:
            if get_has_messages(html_text):
                html_messages_text = get_html_text(get_response(messages=True))
                messages = get_messages(html_messages_text) 
        except Exception:
            return {}

    if response:
        send_email(response)
    
    if messages:
        response['messages'] = messages
        for message in messages[::-1]:
            send_message_email(**message)

    log("chage data" if response else "{}")
    return response


@app.route('/pause')
def pause():
    update_to_key(key='pause', value='paused')
    return ''


@app.route('/resume')
def resume():
    update_to_key(key='pause', value='not paused')
    return ''


def run():
    init()
    app.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    run()

import os

from dotenv import load_dotenv
from flask import Flask

from log import log, get_last_log
from mailsender import send_email, send_wrong_cookie_email
from parser import response_api, get_html_text, get_response

load_dotenv()

app = Flask('')
app.config['JSON_AS_ASCII'] = False
app.secret_key = os.environ['flask_key']


@app.route('/')
def home():
    return get_last_log()


@app.route('/check')
def check():
    response = {}
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

    if response:
        send_email(response)

    log("chage data" if response else "{}")
    return response


def run():
    app.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    run()

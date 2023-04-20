import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
from jinja2 import Environment, BaseLoader

from log import now

load_dotenv()

sender_email = os.environ['sender_email']
receiver_email = os.environ['receiver_email']
password = os.environ['password']


def _send(msg):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg)


def message(subject, attach):
    _message = MIMEMultipart('alternative')
    _message['Subject'] = subject
    _message['From'] = sender_email
    _message['To'] = receiver_email
    _message.attach(attach)
    return _message


def send_email(data):
    d = now().strftime('%d %b, %Y')
    data['dif_keys'] = [k for k, v in data['deltas'].items() if v]

    subject = ', '.join(data['dif_keys'])
    if subject:
        subject = f'{d} {subject}'
    else:
        subject = f'initial grades {d}'

    with open('mail_template.html', 'r', encoding='utf-8') as f:
        template = f.read()

    rtemplate = Environment(loader=BaseLoader).from_string(template)
    html = rtemplate.render(data=data)

    m = message(subject, MIMEText(html, 'html'))

    _send(m.as_string())


def send_wrong_cookie_email():
    text = """hi. please change cookie on .env file"""
    m = message('wrong cookie', MIMEText(text, 'text'))

    _send(m.as_string())


def send_message_email(title, message_text, url):
    html = f"""\
    <html>
      <body>
        <h2>{title}</h2>
        <p style="font-size: 14px;">{message_text}</p>
        <a href={url}>{url}<a/>
      </body>
    </html>
    """
    m = message(
        subject=title.replace('გამომგზავნი', 'CR Message'), 
        attach=MIMEText(html, 'html')
    )

    _send(m.as_string())

import logging
import smtplib
import ssl
from configparser import ConfigParser
from email.message import EmailMessage

logger = logging.getLogger(__name__)

config = ConfigParser()
config.read('creds.ini')
defaults = config.defaults()

msg = EmailMessage()
msg.set_content('test content')
msg['Subject'] = 'test subject'
msg['From'] = defaults['from_email']
msg['To'] = defaults['to_email']

server = smtplib.SMTP('smtp.gmail.com', 587)
context = ssl.create_default_context()
server.starttls(context=context)
server.login(defaults['from_email'], defaults['pw'])
server.send_message(msg)
server.quit()

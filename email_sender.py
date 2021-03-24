import logging
import smtplib
import ssl
from configparser import ConfigParser
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import strftime

logger = logging.getLogger(__name__)

config = ConfigParser()
config.read('creds.ini')
defaults = config.defaults()

def send_email(results):
    msg = MIMEMultipart("alternative")
    msg['Subject'] = 'arXiv digest'
    msg['From'] = defaults['from_email']
    msg['To'] = defaults['to_email']

    body = build_body(results)
    # client should attempt to render the last part first
    msg.attach(MIMEText(body, 'plain'))
    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls(context=ssl.create_default_context())
            server.login(defaults['from_email'], defaults['pw'])
            server.send_message(msg)
    except Exception as e:
        logger.exception(e)
        raise e

def build_body(results):
    """Construct raw HTML of the email body."""
    body = "<html><body>"
    for section in results:
        body += "<section>"
        body += f"<hr><h2>{section}</h2><hr>"
        for author in results[section]:
            for paper in results[section][author]:
                body += f"<h3>{paper['title']}</h3>"
                body += f"<p>{', '.join(paper['authors'])}</p>"
                submitted = paper['published_parsed']
                updated = paper['updated_parsed']
                if submitted == updated:
                    body += f"<p><i>submitted: {strftime('%a %b %d, %Y', submitted)}</i></p>"
                else:
                    body += f"<p><i>updated: {strftime('%a %b %d, %Y', updated)} (submitted: {strftime('%b %d, %Y', submitted)})</i></p>"
                body += f"<a href={paper['arxiv_url']}>{'/'.join(paper['arxiv_url'].split('/')[-2:])}</a> (<a href={paper['pdf_url']}>pdf</a>)"
                body += f"<p><b>abstract:</b> {paper['summary']}</p>"
        body += "</section>"
    body += "</body></html>"
    return body

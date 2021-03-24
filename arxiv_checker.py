import logging
from configparser import ConfigParser
from datetime import timedelta, datetime
from calendar import timegm
from sys import exit

import arxiv

from query_builder import build_author_query
from email_sender import send_email


logging.basicConfig(filename='info.log', level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)

db = ConfigParser()
db.read('database.ini')
last_digest = datetime.fromtimestamp(float(db['DEFAULT']['last digest']))
now = datetime.now()
# send a digest once every Monday, or after 1 week has elapsed
if last_digest.date() == now.date():
    logger.info(f"Abort: already sent a digest today")
    exit()
if now.weekday() != 0 and now - last_digest < timedelta(weeks=1):
    logger.info("Abort: it's not Monday, and it's been less than a week since last digest")
    exit()

config = ConfigParser(allow_no_value=True)
config.read('config.ini')
results = {}
logger.info('Checking arXiv...')
try:
    for section in config.sections():
        results[section] = {}
        for author in config[section].keys():
            # arxiv returns times in UTC, timegm converts UTC to seconds since the epoch,
            # and fromtimestamp converts seconds since the epoch to a local datetime
            results[section][author] = [paper for paper in arxiv.query(query=build_author_query(author), max_results=1, sort_by="lastUpdatedDate", sort_order="descending") if datetime.fromtimestamp(timegm(paper['updated_parsed'])) >= last_digest]
except Exception as e:
    logger.exception(e)
    logger.error("...abort: a query failed")
    exit()

if not all([len(results[section][author]) == 0 for section in results for author in results[section]]):
    try:
        send_email(results)
        logger.info('...email sent')
    except:
        logger.error('...abort: failed to send email.')
        exit()

try:
    db['DEFAULT']['last digest'] = str(now.timestamp())
    with open('database.ini', 'w') as dbfile:
        db.write(dbfile)
except Exception as e:
    logger.exception(e)
    logger.error('...abort: failed to update last digest time')
    exit()

# TODO limit future queries after last digest time
# TODO increase max_results
# run periodically...

logger.info('...done.')

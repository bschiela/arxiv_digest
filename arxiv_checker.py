import logging
from configparser import ConfigParser

import arxiv

from query_builder import build_author_query

logging.basicConfig(filename='info.log', level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)
logger.info('Checking arXiv...')

config = ConfigParser(allow_no_value=True)
config.read('config.ini')

results = {}
for section in config.sections():
    results[section] = []
    for author in config[section].keys():
        results[section].append(
                arxiv.query(
                    query=build_author_query(author),
                    max_results=1,
                    sort_by="lastUpdatedDate",
                    sort_order="descending"
                )
        )
logger.info('...done.')

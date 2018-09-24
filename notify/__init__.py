import os, urllib.request as request
from . import helper
from . import logger

from . vars import *

try:
    logger.info('Getting data from Dynalist server.')
    req = request.Request(config['DYNALIST_URL'], data=params, headers=headers)
    resp = request.urlopen(req)
    fetch_stat = resp.read().decode('utf-8')
    process = True
    logger.info('Connected to Dynalist server.')
except Exception:
    logger.critical('Unable to connect to Dynalist.')
    logger.warning('Exiting...')
    exit()
finally:
    if process:
        data = json.loads(fetch_stat)
        if data['_code'] == 'Ok':
            logger.info('Data fetched from Dynalist server.')
            logger.info('Saving data...')
            save = helper.save(data)
            if save:
                logger.info('All data saved')
                logger.info('Parsing data...')
                helper.parse(save[0], save[1])
        else:
            logger.critical(data['_msg'])
            logger.warning('Exiting...')
            exit()

logger.info('Removing old file, "old.txt".')
os.remove('old.txt') # remove old.txt to replace it with new fresh one after rendering
logger.info('Removed "old.txt"')
logger.info('Renaming "new.txt" to "old.txt"')
os.rename('new.txt', 'old.txt') # rename new.txt with old.txt for later use
logger.info('Renamed.')
logger.info('Cycle completed.')
logger.info('Exiting...')
exit()

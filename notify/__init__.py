import urllib.request as request
import logging
from . helper import save
from vars import *
from app import config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s: %(name)s: %(message)s - %(asctime)s')

file_handler = logging.FileHandler(os.path.join(config['RESOURCES_PATH'], 'notify.log'))
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


try:
    logger.info('Getting data from Dynalist server.')
    req = request.Request(config['DYNALIST_URL'], data=params, headers=headers)
    resp = request.urlopen(req)
    fetch_stat = resp.read().decode('utf-8')
    process = True
    logger.info('Connected to Dynalist server.')
except:
    logger.critical('Unable to connect to Dynalist.')
    logger.warning('Exiting...')
    exit()
finally:
    if process:
        data = json.loads(fetch_stat)
        if data['_code'] == 'Ok':
            logger.info('Data fetched from Dynalist server.')
            logger.info('Saving data...')
            files = save(data)
        else:
            logger.critical(data['_msg'])
            logger.warning('Exiting...')
            exit()

logger.info('Removing old file, "old.txt".')
os.remove(old_file)  # remove old.txt to replace it with new fresh one after rendering
logger.info('Removed "old.txt"')
logger.info('Renaming "new.txt" to "old.txt"')
os.rename(new_file, old_file)  # rename new.txt with old.txt for later use
logger.info('Renamed.')
logger.info('Cycle completed.')
logger.info('Exiting...')
with open(os.path.join(config['RESOURCES_PATH'], 'notify.log'), 'a') as f:
    f.write('\n\n')
exit()

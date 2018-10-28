import logging
from app import config
from . helper import save
from os import path, remove, rename
from app.models import get_dynalist_data

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s: %(name)s: %(message)s - %(asctime)s')

file_handler = logging.FileHandler(path.join(config['RESOURCES_PATH'], 'notify.log'))
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

data = get_dynalist_data()

if type(data) is dict:
    save(data)
else:
    logger.critical(data)
    logger.critical('Exiting..')
    exit(1)

logger.info('Removing old file, "old.txt".')
remove(config['OLD_FILE'])  # remove old.txt to replace it with new fresh one after rendering
logger.info('Removed "old.txt"')
logger.info('Renaming "new.txt" to "old.txt"')
rename(config['NEW_FILE'], config['OLD_FILE'])  # rename new.txt with old.txt for later use
logger.info('Renamed.')
logger.info('Cycle completed.')
logger.info('Exiting...')
with open(path.join(config['RESOURCES_PATH'], 'notify.log'), 'a') as f:
    f.write('\n\n')
exit()

import logging
from app import config
from . helper import save, parse
from os import path, remove, rename
from app.models import get_dynalist_data, AppSettings

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
app_sett = AppSettings.query.get('core')


def run(dry_run):
    if type(data) is dict:
        files = save(data)
        logger.info('Parsing...')
        parse(files[0], files[1], dry_run)
    else:
        logger.critical(data)
        logger.critical('Exiting..')
        exit(1)

    logger.info('Removing old file, "old.txt".')
    remove(app_sett.old_file)  # remove old.txt to replace it with new fresh one after rendering
    logger.info('Removed "old.txt"')
    logger.info('Renaming "new.txt" to "old.txt"')
    rename(app_sett.new_file, app_sett.old_file)  # rename new.txt with old.txt for later use
    logger.info('Renamed.')
    logger.info('Cycle completed.')
    logger.info('Exiting...')


with open(path.join(config['RESOURCES_PATH'], 'notify.log'), 'a') as f:
    f.write('\n\n')

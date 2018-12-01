from os import path, remove
from json import dump
from datetime import datetime
import logging
from .g_drive_api import google_drive_upload
from app import config
from app.models import get_dynalist_data, AppSettings

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s: %(name)s: %(message)s - %(asctime)s')

file_handler = logging.FileHandler(path.join(config['RESOURCES_PATH'], 'backup.log'))
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

app_sett = AppSettings.query.get('core')


def run():
    if not app_sett.backup_enabled:
        logger.warning('Backup task initialized but disabled in settings.')
        logger.warning('Exiting')
        exit()
    data = get_dynalist_data()
    if type(data) is dict:
        file_name = f'{app_sett.backup_file_prefix}.{datetime.utcnow().date()}.T{datetime.utcnow().hour}'\
                    f'{datetime.utcnow().minute}Z.json'  # file name: Edgeryders.DynalistTasks.2019.01.01.T0000Z.json
        backup_file = path.join(app_sett.backup_dir, file_name)
        try:
            with open(backup_file, 'w') as f:
                dump(data['nodes'], f)
                logging.info(f'Saved as { backup_file }')
        except Exception as e:
            logging.critical(e)
        if app_sett.backup_type == 2:
            google_drive_upload(backup_file)
            remove(backup_file)  # delete file from disk
            logging.info('Backup file deleted from disk.')
    else:
        logging.critical(data)
        logging.critical('Exiting...')

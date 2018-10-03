import os
from datetime import date
from . g_drive_api import upload
from app import config


filename = f'Dynalist.EdgerydersTasks.{date.today()}.json'
backup_file = os.path.join(config['RESOURCES_PATH'], filename)
gdrive_dir = config['GOOGLE_DRIVE_DIR_ID']

upload(backup_file, gdrive_dir)

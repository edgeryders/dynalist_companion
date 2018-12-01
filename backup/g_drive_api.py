from os import path
import logging
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload
from app import config
from app.models import AppSettings

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


def google_drive_upload(file_path):
    if not path.isfile(file_path):  # Check if uploading file exists
        logger.critical(f'{file_path} not found.')  # log file not found error and exit
        exit(1)
    scopes = 'https://www.googleapis.com/auth/drive'
    store = file.Storage(path.join(config['RESOURCES_PATH'], 'token.json'))
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(path.join(config['RESOURCES_PATH'], 'credentials.json'), scopes)
        creds = tools.run_flow(flow, store)
    drive_service = build('drive', 'v3', http=creds.authorize(Http()))
    if path.isfile(file_path): # Check if file exists
        upload_file = file_path
        gdrive_dir = [app_sett.google_drive_id]  # Google drive directory id from database
        file_name = path.basename(open(file_path).name)  # get filename from path

        file_metadata = {
            'name': file_name,
            'parents': gdrive_dir,
            'description': 'Dynalist backup'
        }
        media = MediaFileUpload(upload_file)
        file_create = drive_service.files().create(
                                            body=file_metadata,media_body=media,
                                            fields='id').execute()
        logger.info(f"File {file_create.get('id')} uploaded to {app_sett.google_drive_id}")

import os
import json
import logging
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload
from app import config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s: %(name)s: %(message)s - %(asctime)s')

file_handler = logging.FileHandler(os.path.join(config['RESOURCES_PATH'], 'backup.log'))
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

def upload(file_path, gdir):
    SCOPES = 'https://www.googleapis.com/auth/drive'
    store = file.Storage(os.path.join(config['RESOURCES_PATH'], 'token.json'))
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(os.path.join(config['RESOURCES_PATH'], 'credentials.json'), SCOPES)
        creds = tools.run_flow(flow, store)
    drive_service = build('drive', 'v3', http=creds.authorize(Http()))
    if os.path.isfile(file_path): # Check if file exists
        upload_file = file_path
        gdrive_dir = [gdir] # Google drive directory id
        file_name = os.path.basename(open(file_path).name)  # get filename from path

        file_metadata = {
        'name': file_name,
        'parents': gdrive_dir,
        'description': 'files backup'
        }
        media = MediaFileUpload(upload_file)
        file_create = drive_service.files().create(
                                            body=file_metadata,media_body=media,
                                            fields='id').execute()
        print(f"File {file_create.get('id')} uploaded to gdrive_dir")

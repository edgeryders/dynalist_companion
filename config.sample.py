import os

APP_NAME = 'Edgeryders'
PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))
DATABASE_PATH = os.path.join(PROJECT_PATH, 'resources', '')

DEBUG = False
PORT = 8080
SMTP_HOST = 'smtp.gmail.com'
SMTP_EMAIL = 'YOUR GMAIL Address'
SMTP_PASSWORD = 'YOUR GMAIL PASSWORD'
SMTP_PORT = 587
DYNALIST_URL = 'https://dynalist.io/api/v1/doc/read'
DYNALIST_API_TOKEN = 'DYNALIST TOKEN'
DYNALIST_FILE_ID = 'DYNALIST FILE ID'
SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}database.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

import os

APP_NAME = 'Edgeryders'
PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))
RESOURCES_PATH = os.path.join(PROJECT_PATH, 'resources', '')

DEBUG = False
PORT = 8080
SMTP_HOST = 'smtp.gmail.com'
SMTP_EMAIL = 'YOUR EMAIL ADDRESS'
SMTP_PASSWORD = 'YOUR EMAIL PASSWORD'
SMTP_PORT = 587
DYNALIST_URL = 'https://dynalist.io/api/v1/doc/read'
DYNALIST_API_TOKEN = 'DYNALIST TOKEN'
DYNALIST_FILE_ID = 'DYNALIST FILE ID'
SQLALCHEMY_DATABASE_URI = f'sqlite:///{RESOURCES_PATH}database.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

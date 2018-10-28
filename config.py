from os import path

APP_NAME = 'Edgeryders'
PROJECT_PATH = path.dirname(path.realpath(__file__))
RESOURCES_PATH = path.join(PROJECT_PATH, 'resources', '')
OLD_FILE = path.join(RESOURCES_PATH, 'old.txt')
NEW_FILE = path.join(RESOURCES_PATH, 'new.txt')
DYNALIST_BACKUP_DIR = path.join(RESOURCES_PATH, 'dynalist_backup')
PORT = 8080
SQLALCHEMY_DATABASE_URI = f'sqlite:///{RESOURCES_PATH}database.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

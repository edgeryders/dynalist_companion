from os import path

VERSION = '1.5.0'
PROJECT_PATH = path.dirname(path.realpath(__file__))
RESOURCES_PATH = path.join(PROJECT_PATH, 'resources', '')
SQLALCHEMY_DATABASE_URI = f'sqlite:///{RESOURCES_PATH}database.db'
SECRET_KEY = '2c40dd97b6ccb15bb7719892b7f3208c'

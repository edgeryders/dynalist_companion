import json, os
from app import app

config = app.config
process = None
old_file = os.path.join(config['PROJECT_PATH'], 'resources', 'old.txt')
new_file = os.path.join(config['PROJECT_PATH'], 'resources', 'new.txt')

body = {
    'token': config['DYNALIST_API_TOKEN'],
    'file_id': config['DYNALIST_FILE_ID']
     }
params = json.dumps(body).encode('utf-8')
headers = {'Content-Type': 'application/json', 'User-Agent': 'Debendra Bot'}

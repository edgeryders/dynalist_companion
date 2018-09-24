import argparse, json
from app import app
parser = argparse.ArgumentParser()
parser.add_argument('--dry-run', action='store_true', help='Test notification in dry run mode.')

args = parser.parse_args()

dry_run = args.dry_run

config = app.config
process = None

body = {
    'token': config['DYNALIST_API_TOKEN'],
    'file_id': config['DYNALIST_FILE_ID']
     }
params = json.dumps(body).encode('utf-8')
headers = {'Content-Type': 'application/json', 'User-Agent': 'Debendra Bot'}

import json, os, urllib.request as request
from app import app
from notify import helper

config = app.config
process = None
body = {
    'token': config['DYNALIST_API_TOKEN'],
    'file_id': config['DYNALIST_FILE_ID']
     }
params = json.dumps(body).encode('utf-8')
headers = {'Content-Type': 'application/json', 'User-Agent': 'Debendra Bot'}

try:
    req = request.Request(config['DYNALIST_URL'], data=params, headers=headers)
    resp = request.urlopen(req)
    fetch_stat = resp.read().decode('utf-8')
    process = True
except Exception:
    print('Unable to connect to dynalist')
    exit()
finally:
    if process:
        data = json.loads(fetch_stat)
        if data['_code'] == 'Ok':
            save = helper.save(data)
            if save:
                helper.parse(save[0], save[1])
        else:
            print(data['_msg'])
            exit()

os.remove('old.txt') # remove old.txt to replace it with new fresh one after rendering
os.rename('new.txt', 'old.txt') # rename new.txt with old.txt for later use
exit()

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
except:
    print('Unable to connect to dynalist')
    exit()
finally:
    if process:
        load_json = json.loads(fetch_stat)
        if load_json['_code'] == 'Ok':
            data = load_json
            save = helper.save(data)
            if save:
                helper.parse(save[0], save[1])
        else:
            print(load_json['_msg'])
            exit()

os.remove('dynalist-a.txt') # remove dynalist-a.txt to replace it with new fresh one after rendering
os.rename('dynalist-b.txt', 'dynalist-a.txt') # rename dynalist-b.txt with dynalist-a.txt for later use
exit()

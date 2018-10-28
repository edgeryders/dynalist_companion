from . import db, login_manager
import re
from datetime import datetime
from app import config
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    browser_pushid = db.Column(db.Text)
    push_email = db.Column(db.SmallInteger, default='1')
    push_web = db.Column(db.SmallInteger, default='1')
    alert_deadline = db.Column(db.Integer, default='1')
    is_admin = db.Column(db.SmallInteger, default='0')


def deadlines(username):
    try:
        read_file = open(config['OLD_FILE'], 'r', encoding='utf-8').read()
        dates = re.findall('.*(20[0-9]{2}-\d{2}-\d{2}).*\.\s.*#%s' % username, read_file)
        dates = [datetime.strptime(date, '%Y-%m-%d') for date in dates]
        now = datetime.now()

        past_dates = [date for date in dates if date < now]
        last_deadline = max(date for date in dates if date < now) if past_dates else 'None'

        future_dates = [date for date in dates if date > now]
        next_deadline = min(date for date in dates if date > now) if future_dates else 'None'

        return {'last': str(last_deadline)[:10], 'next': str(next_deadline)[:10]}

    except FileNotFoundError:

        return {'last': 'None', 'next': 'None'}


class AppSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    backup_enabled = db.Column(db.SmallInteger)
    backup_type = db.Column(db.SmallInteger)  # 1 = drive, 2 = google drive
    google_drive_id = db.Column(db.String())
    backup_file_prefix = db.Column(db.String())
    email_push_enabled = db.Column(db.SmallInteger)  # 1 = enabled, 0 = disabled
    web_push_enabled = db.Column(db.SmallInteger)  # 1 = enabled, 0 = disabled
    dynalist_api_token = db.Column(db.String())
    dynalist_api_url = db.Column(db.String())
    dynalist_api_file_id = db.Column(db.String())
    smtp_host = db.Column(db.String())
    smtp_port = db.Column(db.Integer)
    smtp_email = db.Column(db.String())
    smtp_password = db.Column(db.String())
    secret_code = db.Column(db.String())


def get_dynalist_data():
    from urllib import request
    from json import dumps, loads
    from app import app_sett

    body = {
        'token': app_sett.dynalist_api_token,
        'file_id': app_sett.dynalist_api_file_id
    }
    params = dumps(body).encode('utf-8')
    headers = {'Content-Type': 'application/json', 'User-Agent': 'Debendra Bot'}
    try:
        req = request.Request(app_sett.dynalist_api_url, data=params, headers=headers)
        resp = request.urlopen(req)
        raw_data = resp.read().decode('utf-8')
    except Exception as e:
        return e
    finally:
        load_data = loads(raw_data)
        if load_data['_code'] == 'Ok':
            return load_data
        else:
            return load_data['_msg']


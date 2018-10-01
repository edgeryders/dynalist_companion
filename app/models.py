from . import db
import re
from datetime import datetime


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    browser_pushid = db.Column(db.Text)
    push_email = db.Column(db.Integer, default='1')
    push_web = db.Column(db.Integer, default='1')
    alert_deadline = db.Column(db.Integer, default='1')


class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(1), unique=True)
    name = db.Column(db.String())
    example = db.Column(db.Text)


def deadlines(username):
    try:
        read_file = open('old.txt', 'r', encoding='utf-8').read()
        dates = re.findall('.*(20[0-9]{2}-\d{2}-\d{2}).*. #[%s]' % username, read_file)
        dates = [datetime.strptime(date, '%Y-%m-%d') for date in dates]
        now = datetime.now()
        last_deadline, next_deadline = max(date for date in dates if date < now), min(date for date in dates if date > now)
        return {'last': last_deadline, 'next': next_deadline}
    except FileNotFoundError:
        return {'last': 'None', 'next': 'None'}

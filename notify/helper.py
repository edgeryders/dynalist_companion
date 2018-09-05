import os
import re
from app.models import Users
import json
from app import config


def save(data):

    '''
    Content fetched from dynalist api will be saved in server
    '''
    files = []
    if not os.path.isfile('old.txt'):
        old = open('old.txt', 'w', encoding='utf-8')
        for lines in data['nodes']:
            if lines['checked'] == False:
                old.write(f"{lines['id']} || {lines['content'].rstrip()}\n")
        old.close()
        exit()
    else:
        new = open('new.txt', 'w', encoding='utf-8')
        for lines in data['nodes']:
            if lines['checked'] == False:
                new.write(f"{lines['id']} || {lines['content'].rstrip()}\n")
        new.close()
        files = ['old.txt', 'new.txt']

    return files


def get_email(username): #get email address from database using tag we got from dynalist
    email = False
    req = Users.query.filter_by(username=username).first()
    if req:
        email = req.email
    return email


def parse(old, new):
    '''
    Compare two files dynalist-a.txt (old) and dynalist-b.txt (new) that were previously saved before by save().
    '''
    old_file = open(old, 'r', encoding='utf-8').readlines()
    new_file = open(new, 'r', encoding='utf-8').readlines()
    diff = [line for line in new_file if line not in old_file]
    if diff:
        assigns = []
        mentions = []
        for line in diff:
            if line.count('@'):
                mentions += re.findall('\s@([a-z.]+)', line)
            elif line.count('#'):
                assigns += re.findall('\s#([a-z.]+)', line)

            if mentions:
                for mention in mentions:
                    email = get_email(mention)
                    if email:
                       split_content = line.split(' || ')
                       url = f"https://dynalist.io/d/{config['DYNALIST_FILE_ID']}#z={split_content[0]}"
                       sendmail('Dynalist Notifications: New Mention', email,
                                      f'Hi {mention},\n\nYou have been mentioned in a new task:\n\n"{split_content[1]}"\n{url}\nGood luck :)')
            if assigns:
                for assign in assigns:
                    email = get_email(assign)
                    if email:
                        split_content = line.split(' || ')
                        url = f"https://dynalist.io/d/{config['DYNALIST_FILE_ID']}#z={split_content[0]}"
                        sendmail('Dynalist Notifications: New Task', email,
                                      f'Hi {assign},\n\nYou have been assigned a new task:\n\n"{split_content[1]}"\n{url}\nGood luck :)')


def sendmail(subject, emailto, message): # Send email
    from app import config
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import smtplib
    msg = MIMEMultipart()
    fromaddr = config['SMTP_EMAIL']
    msg['From'] = fromaddr
    msg['To'] = emailto
    msg['Subject'] = subject
    password = config['SMTP_PASSWORD']
    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP(config['SMTP_HOST'], config['SMTP_PORT'])
    server.starttls()
    server.login(fromaddr, password)
    body = msg.as_string()
    server.sendmail(fromaddr, emailto, body)
    server.quit()

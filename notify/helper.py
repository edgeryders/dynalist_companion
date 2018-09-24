import os
import re
from app.models import Users
from . import logger
from . vars import dry_run, config


def save(data):

    '''
    Content fetched from dynalist api will be saved in server
    '''
    files = []
    if not os.path.isfile('old.txt'):
        logger.info('Writing old.txt')
        old = open('old.txt', 'w', encoding='utf-8')
        for lines in data['nodes']:
            if lines['checked']:
                old.write(f"{lines['id']} || {lines['content'].strip()}\n")
        old.close()
        logger.info('"old.txt" written.')
        logger.info('Exiting...')
        exit()
    else:
        logger.info('Writing new.txt')
        new = open('new.txt', 'w', encoding='utf-8')
        for lines in data['nodes']:
            if lines['checked']:
                new.write(f"{lines['id']} || {lines['content'].strip()}\n")
        new.close()
        files = ['old.txt', 'new.txt']
        logger.info('new.txt written.')
    return files


def get_email(username):  # get email address from database using tag we got from dynalist
    email = False
    logger.info(f'getting email address for {username}')
    req = Users.query.filter_by(username=username, push_email=1).first()
    if req:
        email = req.email
        logger.info(f'Found {email} for {username}.')
    return email


def parse(old, new):  # Compare two files dynalist-a.txt (old) and dynalist-b.txt (new) that were previously saved before by save().
    logger.info('reading old.txt.')
    old_file = open(old, 'r', encoding='utf-8').readlines()
    logger.info('reading new.txt.')
    new_file = open(new, 'r', encoding='utf-8').readlines()
    diff = [line for line in new_file if line not in old_file]
    if diff:
        logger.info('New tasks found.')
        logger.info('Parsing...')
        assigns = []
        mentions = []
        for line in diff:
            if line.count('@'):
                mentions = re.findall('\s@([a-z.]+)', line)
            if line.count('#'):
                assigns = re.findall('\s#([a-z.]+)', line)

            if mentions:
                for mention in mentions:
                    email = get_email(mention)
                    if email:
                        logger.info(f'Sending mail to {mention}, address {email}')
                        if not dry_run:
                            sendmail('Dynalist Notifications: New Mention', email,
                                     f'Hi {mention},\n\nYou have been mentioned in a new task:"\n\n{split_content[1]}"\n{url}\nGood luck :)')
            if assigns:
                for assign in assigns:
                    email = get_email(assign)
                    if email:
                        logger.info(f'Sending mail to {assign}, address {email}')
                        split_content = line.split(' || ')
                        url = f"https://dynalist.io/d/{config['DYNALIST_FILE_ID']}#z={split_content[0]}"
                        if not dry_run:
                            sendmail('Dynalist Notifications: New Task', email,
                                      f'Hi {assign},\n\nYou have been assigned a new task:"\n\n{split_content[1]}"\n{url}\nGood luck :)')



def sendmail(subject, emailto, message): # Send email
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

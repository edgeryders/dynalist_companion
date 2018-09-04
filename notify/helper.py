import os
import re
from app.models import Users


def save(data):

    '''
    Content fetched from dynalist api will be saved in server
    '''
    files = []
    if not os.path.isfile('dynalist-a.txt'):
        a_file = open('dynalist-a.txt', 'w', encoding='utf-8')
        for lines in data['nodes']:
            if lines['checked'] == False:
                a_file.write(f"{lines['content']}\n")
        a_file.close()
        exit()
    else:
        b_file = open('dynalist-b.txt', 'w', encoding='utf-8')
        for lines in data['nodes']:
            if lines['checked'] == False:
                b_file.write(f"{lines['content']}\n")
        b_file.close()
        files = ['dynalist-a.txt', 'dynalist-b.txt']

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
    oldfile = open(old, 'r', encoding='utf-8')
    newfile = open(new, 'r', encoding='utf-8')
    diff = [line for line in newfile if line not in oldfile]
    if diff:
        assigns = []
        mentions = []
        for line in diff:
            if line.count('@'):
                mentions += re.findall('\s@([a-z]{3,15})', line)
            elif line.count('#'):
                assigns += re.findall('\s#([a-z]{3,15})', line)
            if mentions:
                for mention in mentions:
                    email = get_email(mention)
                    if email:
                        sendmail('Dynalist Notifications: New Mention', email,
                                      f'Hi {mention},\n\nYou have been mentioned in a new task:\n\n"{line}"\nGood luck :)')
            if assigns:
                for assign in assigns:
                    email = get_email(assign)
                    if email:
                        sendmail('Dynalist Notifications: New Task', email,
                                      f'Hi {assign},\n\nYou have been assigned a new task:\n\n"{line}"\nGood luck :)')


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

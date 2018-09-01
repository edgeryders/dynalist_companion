import os
import re
from app.models import Users


def save(data):

    files = []
    '''
    Content fetched from dynalist api will be saved in server
    '''
    if not os.path.isfile('dynalist-a.txt'):
        a_file = open('dynalist-a.txt', 'w', encoding='utf-8')
        for lines in data['nodes']:
            if lines['checked'] == False:
                a_file.write('%s\n' % lines['content'])
        a_file.close()
        exit()
    else:
        b_file = open('dynalist-b.txt', 'w', encoding='utf-8')
        for lines in data['nodes']:
            if lines['checked'] == False:
                b_file.write('%s\n' % lines['content'])
        b_file.close()
        files = ['dynalist-a.txt', 'dynalist-b.txt']

    return files


def get_email(username): #get email address from database using tag we got from dynalist
    email = False
    req = Users.query.filter_by(username=username).one()
    if req:
        email = req.email
    return email


def parse(file1, file2):
    '''
    Compare two files dynalist-a.txt (old) and dynalist-b.txt (new) that were previously saved before by save().
    '''
    file1 = open(file1, 'r', encoding='utf-8')
    file2 = open(file2, 'r', encoding='utf-8')
    read_file1 = file1.readlines()
    read_file2 = file2.readlines()
    diff = [line for line in read_file1 if line not in read_file2]
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
                        sendmail('[Dynalist Notification Mentions]', email,
                                      f'Hi {mention},\nYou have been mentioned in a new task.\n\n{line}\nGood luck.:)')
            if assigns:
                for assign in assigns:
                    email = get_email(assign)
                    if email:
                        sendmail('[Dynalist Notification New Task]', email,
                                      f'Hi {assign},\nYou have been assigned with a new task.\n\n{line}\nGood luck. :)')


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
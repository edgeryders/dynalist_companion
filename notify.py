import urllib.request as request
import json
import os
import datetime
from time import sleep
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sqlite3



class Notifier():
	conf = ''
	conn = False
	data = ''
	process = False

	def __init__(self):
		try:
			self.conn = sqlite3.connect('users.db')
		except:
			print('error')
		conf = open('conf.json', 'r')
		self.conf = json.load(conf)
		url = self.conf['dynalist']['url']
		body = {
		'token': self.conf['dynalist']['api'],
		'file_id': self.conf['dynalist']['file_id']
		}
		params = json.dumps(body).encode('utf-8')
		headers = {'Content-Type': 'application/json', 'User-Agent': 'Debendra Bot'}

		try:
			req = request.Request(url, data=params, headers=headers)
			resp = request.urlopen(req)
			fetch_stat = resp.read().decode('utf-8')
			self.process = True

		except:
			print('Unable to connect to dynalist')

		finally:
			if self.process:
				load_json = json.loads(fetch_stat)
				if load_json['_code'] == 'Ok':
					self.data = load_json
					full_file = open('dynalist-full.json', 'w')
					full_file.write(json.dumps(self.data['nodes']))
					full_file.close()
					self.save()
				else:
					print(load_json['_msg'])
 
	def save(self):
		if not os.path.isfile('dynalist-a.txt'):
			a_file = open('dynalist-a.txt', 'w')
			for lines in self.data['nodes']:
				if lines['checked'] == False:
					a_file.write('%s\n' % lines['content'])
			a_file.close()
			sleep(600)
			self.save()
		else:
			'''created_time = datetime.datetime.fromtimestamp(os.path.getmtime('dynalist-a.txt'))
			now_time = datetime.datetime.now() - created_time
			get_minute = int(now_time.total_seconds() / 60)
			if get_minute > 1:'''
			b_file = open('dynalist-b.txt', 'w')
			for lines in self.data['nodes']:
				if lines['checked'] == False:
					b_file.write('%s\n' % lines['content'])
			b_file.close()
			self.parse()
			'''else:
				sleep(10)
				self.save()'''

	def getemail(self, tag):
		with self.conn:
			cur = self.conn.cursor()
			cur.execute("SELECT email FROM users WHERE tags =?", (tag,))
			email = cur.fetchone()
			if email:
				return email[0]
			else:
				return False

	def parse(self):
		file1 = open('dynalist-a.txt', 'r')
		file2 = open('dynalist-b.txt', 'r')
		file1 = file1.readlines()
		file2 = file2.readlines()
		diff = [x for x in file1 if x not in file2]
		if diff:
			for line in diff:
				res1, res2 = re.search('.{5,}\\.\s#([a-z]{3,15})', line), re.search('.{5,}\\.\s@([a-z]{3,15})', line)
				if res1:
					email = self.getemail(res1.group(1))
					if email:
						self.sendmail('[Dynalist Notification New Task]', email, f'Hi {res1.group(1)},\nYou have been assigned with new task.\n\n{line}\nGood luck.:)')
				elif res2:
					email = self.getemail(res1.group(1))
					if email:
						self.sendmail('[Dynalist Notification Mentions]', email, f'Hi {res1.group(2)},\nYou have been mentioned in a new task.\n\n{line}\nGood luck. :)')
		os.remove('dynalist-a.txt')
		os.rename('dynalist-b.txt', 'dynalist-a.txt')
		self.data = None
		sleep(600)
		self.__init__()


	def sendmail(self, subject, emailto, message):
		msg = MIMEMultipart()
		fromaddr = self.conf['gmail']['email']
		msg['From'] = fromaddr
		msg['To'] = emailto
		msg['Subject'] = subject
		password = self.conf['gmail']['password']
		msg.attach(MIMEText(message, 'plain'))
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(fromaddr, password)
		body = msg.as_string()
		server.sendmail(fromaddr, emailto, body)
		server.quit()


test__ = Notifier()


'''res = f<?xml version="1.0" encoding="utf-8"?>\n
<opml version="2.0">\n
  <head>\n
    <title>{data['title']}</title>\n
    <flavor>dynalist</flavor>\n
    <source>https://dynalist.io</source>\n
    <ownerName></ownerName>\n
    <ownerEmail></ownerEmail>\n
  </head>\n
  <body>\n
for i in body_data:
	res += f    <outline text="{i['content']}" _note="{i['note']}">\n
          \n
 
res += </body>\n
</opml>

save = open('test.txt', 'w')
save.write(res)
save.close()'''

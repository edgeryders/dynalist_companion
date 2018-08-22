import urllib.request as request
import json
import os
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

		conf = open('conf.json', 'r')
		self.conf = json.load(conf)
		try:
			self.conn = sqlite3.connect(self.conf['system']['database'])
		except:
			print('unable to find databse')
			exit()
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
			a_file = open('dynalist-a.txt', 'w', encoding='utf-8')
			for lines in self.data['nodes']:
				if lines['checked'] == False:
					a_file.write('%s\n' % lines['content'])
			a_file.close()
			exit()
		else:
			b_file = open('dynalist-b.txt', 'w', encoding='utf-8')
			for lines in self.data['nodes']:
				if lines['checked'] == False:
					b_file.write('%s\n' % lines['content'])
			b_file.close()
			self.parse()

	def getemail(self, tag):
		with self.conn:
			cur = self.conn.cursor()
			cur.execute("SELECT email FROM users WHERE tag =?", (tag,))
			email = cur.fetchone()
			if email:
				return email[0]
			else:
				return False

	def parse(self):
		file1 = open('dynalist-a.txt', 'r', encoding='utf-8')
		file2 = open('dynalist-b.txt', 'r', encoding='utf-8')
		file1 = file1.readlines()
		file2 = file2.readlines()
		diff = [x for x in file1 if x not in file2]
		assigns = []
		mentions = []
		if diff:
			for line in diff:
				if line.count('@'):
					mentions += re.findall('\s@([a-z]{3,15})', line)
				elif line.count('#'):
					assigns += re.findall('\s#([a-z]{3,15})', line)
				if mentions:
					for mention in mentions:
						email = self.getemail(mention)
						if email:
							self.sendmail('[Dynalist Notification Mentions]', email, f'Hi {mention},\nYou have been mentioned in a new task.\n\n{line}\nGood luck.:)')
				elif assigns:
					for assign in assigns:
						email = self.getemail(assign)
						if email:
							self.sendmail('[Dynalist Notification New Task]', email, f'Hi {assign},\nYou have been assigned with a new task.\n\n{line}\nGood luck. :)')
		os.remove('dynalist-a.txt')
		os.rename('dynalist-b.txt', 'dynalist-a.txt')
		exit()

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


init = Notifier()
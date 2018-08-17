from flask import Flask, render_template, json, request, redirect, url_for, session
import sqlite3
import hashlib
import os
import json

app = Flask(__name__)



def check_password(hashed_password, password):
    return hashed_password == hashlib.md5(password.encode()).hexdigest()

def validate(username, password):
	completion = False
	with sqlite3.connect('users.db') as con:
		cur = con.cursor()
		cur.execute("SELECT password FROM users WHERE username = ?", (username,))
		dbpass = cur.fetchone()
		if dbpass:
			completion = check_password(dbpass[0], password)
			return completion

def registration(username, password, email, dynalist_api, tag):
	with sqlite3.connect('users.db') as con:
		cur = con.cursor()
		cur.execute("SELECT username FROM users WHERE username = ?", (username,))
		exists = cur.fetchone()
		if exists:
			return 'Username already exists.'
		cur.execute("SELECT email FROM users WHERE email = ?", (email,))
		exists = cur.fetchone()
		if exists:
			return 'Email already exists.'
		cur.execute("SELECT tag FROM users WHERE tag = ?", (tag,))
		exists = cur.fetchone()
		if exists:
			return 'Tag already exists.'
		else:
			password = hashlib.md5(password.encode()).hexdigest()
			cur.execute("INSERT INTO users(username, password, email, dynalist_api, tag) VALUES (?, ?, ?, ?, ?)", (username, password, email, dynalist_api, tag,))
			con.commit()
			return True

@app.route('/')
def index():
	if session.get('username'):
		return render_template('index.html')
	else:
		return redirect(url_for('login'))


@app.route('/login', methods=['POST', 'GET'])
def login():
	error = None
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		completion = validate(username, password)
		if not completion:
			error = 'Invalid Credentials. Please try again.'
		else:
			session['username'] = username
			return redirect(url_for('index'))
	return render_template('login.html', error=error)


@app.route('/register', methods=['POST', 'GET'])
def register():
	error = None
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		conf_password = request.form['conf_password']
		dynalist_api = request.form['dynalist_api']
		email = request.form['email']
		tag = request.form['user_tag']
		if not password == conf_password:
			error = 'Password do not match.'
		else:
			register = registration(username, password, email, dynalist_api, tag)
			if register == True:
				session['username'] = username
				return redirect(url_for('index'))
			else:
				error = register
	return render_template('register.html', error=error)



@app.route('/settings')
def settings():
	return render_template('settings.html')

@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('login'))


if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run(debug=True, port=8080)
from flask import render_template, redirect, url_for, session, flash
from app import app, db
from app.models import Users
from app.forms import RegistrationForm, LoginForm, SettingsForm 
import hashlib


@app.route('/')
def index():
    if session.get('username'):
        return render_template('index.html')
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
            user = Users.query.filter_by(username=form.username.data).first()
            if user and hashlib.sha256(form.password.data.encode()).hexdigest() == user.password:
                return redirect(url_for('index'))
            else:
                flash('Invalid credentials', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw = hashlib.sha256(form.password.data.encode()).hexdigest()
        user = Users(username=form.username.data, email=form.email.data, password=hash_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Hi {form.username.data}, Your Account created successfully.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Sign Up', form=form)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    form = SettingsForm()

    return render_template('settings.html', form=form, title='Settings')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

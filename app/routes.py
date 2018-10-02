from flask import render_template, redirect, url_for, session, flash
from . import app, db
from . models import Users, deadlines
from . forms import RegistrationForm, LoginForm, SettingsForm
import hashlib


@app.route('/')
def index():
    username = session.get('username')
    if username:
        users = Users.query.filter(Users.username != username).all()
        taskinfo = deadlines(username)
        return render_template('index.html', title='Home', users=users, taskinfo=taskinfo)
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
            user = Users.query.filter_by(username=form.username.data).first()
            if user and hashlib.sha256(form.password.data.encode()).hexdigest() == user.password:
                session['username'] = user.username
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
        flash(f'Hi {form.username.data}, your account has been created successfully.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Sign Up', form=form)


@app.route('/settings', methods=['GET', 'POST'])
def settings():

    form = SettingsForm()
    user_logged = session.get('username')
    if user_logged:
        get_user = Users.query.filter_by(username=user_logged).first()

        if form.validate_on_submit():
            get_user.username = form.username.data
            get_user.email = form.email.data
            get_user.alert_deadline = form.alert_deadline.data if form.alert_deadline.data else '1'
            get_user.push_email = '1' if form.push_email.data else '0'
            get_user.push_web = '1' if form.push_web.data else '0'
            db.session.commit()
            session['username'] = form.username.data
            flash('Settings updated', 'success')
        else:
            form.username.data = get_user.username
            form.email.data = get_user.email
            form.push_email.data = get_user.push_email
            form.push_web.data = get_user.push_web
            form.alert_deadline.data = get_user.alert_deadline
    else:
        return redirect(url_for('login'))
    return render_template('settings.html', form=form, title='Settings')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

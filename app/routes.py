from flask import render_template, redirect, url_for, flash, abort
from . import app, db, app_sett
from . models import Users, deadlines
from . forms import RegistrationForm, LoginForm, SettingsForm, AppSettingsForm
from flask_login import login_required, login_user, current_user, logout_user
import hashlib


@app.route('/')
@login_required
def index():
    return render_template('index.html', taskinfo=deadlines(current_user.username))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
            user = Users.query.filter_by(username=form.username.data).first()
            if user and hashlib.sha256(form.password.data.encode()).hexdigest() == user.password:
                login_user(user, remember=form.remember.data)
                return redirect(url_for('index'))
            flash('Invalid credentials', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
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
@login_required
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.alert_deadline = form.alert_deadline.data
        current_user.push_email = form.push_email.data
        current_user.push_web = form.push_web.data
        db.session.commit()
        flash('Settings updated', 'success')
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.push_email.data = current_user.push_email
    form.push_web.data = current_user.push_web
    form.alert_deadline.data = current_user.alert_deadline
    return render_template('settings.html', form=form, title='Settings')


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.is_authenticated and current_user.is_admin:
        form = AppSettingsForm()
        if form.validate_on_submit():
            app_sett.backup_enabled = form.backup_enabled.data
            app_sett.backup_type = form.backup_type.data
            app_sett.google_drive_id = form.google_drive_id.data
            app_sett.backup_file_prefix = form.backup_file_prefix.data
            app_sett.email_push_enabled = form.email_push_enabled.data
            app_sett.web_push_enabled = form.web_push_enabled.data
            app_sett.dynalist_api_url = form.dynalist_api_url.data
            app_sett.dynalist_api_token = form.dynalist_api_token.data
            app_sett.dynalist_api_file_id = form.dynalist_api_file_id.data
            app_sett.smtp_host = form.smtp_host.data
            app_sett.smtp_port = form.smtp_port.data
            app_sett.smtp_email = form.smtp_email.data
            app_sett.smtp_password = form.smtp_password.data
            app_sett.secret_code = form.secret_code.data
            db.session.commit()
            flash('Settings applied.', 'success')
        form.backup_enabled.data = app_sett.backup_enabled
        form.backup_type.data = app_sett.backup_type
        form.google_drive_id.data = app_sett.google_drive_id
        form.backup_file_prefix.data = app_sett.backup_file_prefix
        form.email_push_enabled.data = app_sett.email_push_enabled
        form.web_push_enabled.data = app_sett.web_push_enabled
        form.dynalist_api_url.data = app_sett.dynalist_api_url
        form.dynalist_api_token.data = app_sett.dynalist_api_token
        form.dynalist_api_file_id.data = app_sett.dynalist_api_file_id
        form.smtp_host.data = app_sett.smtp_host
        form.smtp_port.data = app_sett.smtp_port
        form.smtp_email.data = app_sett.smtp_email
        form.smtp_password.data = app_sett.smtp_password
        form.secret_code.data = app_sett.secret_code
        return render_template('admin.html', title='Admin panel', form=form)
    abort(404)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

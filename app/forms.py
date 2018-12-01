from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from wtforms.fields.html5 import EmailField
from . models import Users, AppSettings
from flask_login import current_user
from os import path


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20, message='error length')],
                           render_kw={"placeholder": "Username", "autofocus": True})
    email = EmailField('Email', validators=[DataRequired()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),
                                                                     EqualTo('password', 'Password do not match.')],
                                     render_kw={"placeholder": "Confirm Password"})
    secret_code = StringField('Secret Code', validators=[DataRequired()],
                              render_kw={"placeholder": "Secret Code"})
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken.')

    def validate_email(self, email):
        email = Users.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email address already exists.')

    def validate_secret_code(self, secret_code):
        app_sett = AppSettings().query.get('core')
        code = app_sett.secret_code
        if not code == secret_code.data:
            raise ValidationError('Invalid secret code')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()],
                           render_kw={"placeholder": "Username", "autofocus": True})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    remember = BooleanField('Remember Login')
    submit = SubmitField('Login')


class SettingsForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    push_web = BooleanField('Browser Push')
    push_email = BooleanField('Email Push')
    email = EmailField('Email', validators=[DataRequired()])
    alert_deadline = IntegerField('Deadline Alert')
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = Users.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists. Please choose different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Users.query.filter_by(username=email.data).first()
            if user:
                raise ValidationError('Email address already exists. Please choose different one.')


class AppSettingsForm(FlaskForm):
    app_sett = AppSettings.query.get('core')
    backup_enabled = BooleanField('Enable Backup')
    backup_type = SelectField('Backup Type', choices=[('0', 'None'), ('1', 'Drive'), ('2', 'Google Drive')])
    google_drive_id = StringField('Google Drive id')
    backup_file_prefix = StringField('Backup file name prefix')
    email_push_enabled = BooleanField('Enable Email Push')
    web_push_enabled = BooleanField('Enable Web Push')
    dynalist_api_token = StringField('Dynalist Api token')
    dynalist_api_url = StringField('Dynalist Api url')
    dynalist_api_file_id = StringField('Dynalist File id')
    smtp_host = StringField('SMTP Host')
    smtp_port = StringField('SMTP Port')
    smtp_email = StringField('SMTP Email address')
    smtp_password = StringField('SMTP Password')
    secret_code = StringField('Secret Code', validators=[Length(min=8,
                                                                message='Secret code must be greater than 8 in length.')])
    app_name = StringField('App Name')
    old_file = StringField('OLD file')
    new_file = StringField('NEW file')
    backup_dir = StringField('Dynalist Backup Directory')
    submit = SubmitField('Save')

    def validate_old_file(self, old_file):
        if old_file.data != self.app_sett.old_file:
            if not path.isfile(old_file.data):
                raise ValidationError('Old file specified does not exists.')
            elif old_file.data == self.app_sett.new_file:
                raise ValidationError('Old file as same as new file.')

    def validate_new_file(self, new_file):
        if new_file.data != self.app_sett.new_file:
            if not path.isfile(new_file.data):
                raise ValidationError('New file specified does not exists.')
            elif new_file.data == self.app_sett.old_file:
                raise ValidationError('New file as same as old file.')

    def validate_backup_dir(self, backup_dir):
        if backup_dir.data != self.app_sett.backup_dir:
            if not path.isdir(backup_dir.data):
                raise ValidationError('Backup directory specified is not a directory or exists.')

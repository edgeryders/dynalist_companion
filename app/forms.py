from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from wtforms.fields.html5 import EmailField
from . models import Users
from . import app_sett
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20, message='error length')],
                           render_kw={"placeholder": "Username", "autofocus": True})
    email = EmailField('Email', validators=[DataRequired()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),
                                                                     EqualTo('password', 'Passwords do not match.')],
                                     render_kw={"placeholder": "Confirm Password"})
    secret_code = StringField('Secret Code', validators=[DataRequired()],
                              render_kw={"placeholder":"Secret Code"})
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
        code = app_sett.secret_code
        if not code == secret_code.data:
            raise ValidationError('Invalid secret code')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()],
                           render_kw={"placeholder":"Username", "autofocus": True})
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
                raise ValidationError('Username already exists. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Users.query.filter_by(username=email.data).first()
            if user:
                raise ValidationError('Email address already exists. Please choose a different one.')


class AppSettingsForm(FlaskForm):
    backup_enabled = BooleanField('Enable Backup')
    backup_type = SelectField('Backup Type', choices=[('0', 'Backup Type'), ('1', 'Local Folder'), ('2', 'Google Drive')])
    google_drive_id = StringField('Google Drive Folder ID')
    backup_file_prefix = StringField('Backup Filename Prefix')
    email_push_enabled = BooleanField('Enable Email Push')
    web_push_enabled = BooleanField('Enable Web Push')
    dynalist_api_token = StringField('Dynalist API token')
    dynalist_api_url = StringField('Dynalist API URL')
    dynalist_api_file_id = StringField('Dynalist File ID')
    smtp_host = StringField('SMTP Host')
    smtp_port = StringField('SMTP Port')
    smtp_email = StringField('SMTP Email Address')
    smtp_password = StringField('SMTP Password')
    secret_code = StringField('Secret Code', validators=[Length(min=8,
                                                                message='Secret code must be 8 characters or longer.')])
    submit = SubmitField('Save')


#!./venv/bin/python
import argparse


def runserver(args):
    from app import app
    app.run(host=args.host, port=args.port, debug=args.debug)


def notify(args):
    from notify import run
    run(args.dry_run)


def update(args):
    from urllib.request import urlopen
    remote_file = 'https://raw.githubusercontent.com/edgeryders/dynalist_companion/master/update.py'
    try:
        get_remote_content = urlopen(remote_file).read()  # Get update code from github
        exec(get_remote_content)
    except Exception as e:
        print(e)


def backup(args):
    from backup import run
    run()


def usermod(args):
    from app.models import Users
    user = Users.query.filter_by(username=args.username).first()
    if user:
        from app import db
        username_exists = db.session.query(
            db.session.query(Users).filter_by(username=args.new_username).exists()).scalar()
        email_exists = db.session.query(db.session.query(Users).filter_by(email=args.email).exists()).scalar()
        if username_exists:
            print('Username already taken.')
            exit()
        elif email_exists:
            print('Email already exists.')
            exit()
        import hashlib
        import secrets
        user.username = args.new_username if args.new_username else args.username
        passwd = secrets.token_hex(8) if args.rand else args.passwd
        hashed = hashlib.sha256(passwd.encode()).hexdigest()
        user.password = hashed if hashed else user.password
        user.email = args.email if args.email else user.email
        user.is_admin = 1 if args.admin else user.is_admin
        db.session.commit()
        print('User modified successfully.')
        print(f'Username: {user.username}')
        print(f'Email: {user.email}')
        print(f'Password: {passwd}')


parser = argparse.ArgumentParser(
    description='Command line tools for dynalist companion.'
)

parser.add_argument('-V', '--version', action='store_true', help='Check Version.')

subparsers = parser.add_subparsers(help='Available Commands.')

runserver_parser = subparsers.add_parser('runserver', help=False,
                                         description='Run server in localhost.')
runserver_parser.set_defaults(function=runserver)
runserver_parser.add_argument('-D', '--debug', action='store_true',
                              help='Run local web server in debug mode.')
runserver_parser.add_argument('-H', '--host', metavar='IP', default='127.0.0.1',
                              help='Host ip address for local web server.')
runserver_parser.add_argument('-P', '--port', type=int, default=8080,
                              help='Port for local web server.')


update_parser = subparsers.add_parser('update', help=False,
                                      description='Update dynalist companion.')
update_parser.set_defaults(function=update)


notify_parser = subparsers.add_parser('notify', help=False,
                                      description='Run notify extension.')
notify_parser.add_argument('--dry-run', action='store_true', help='Run in dry mode (test).')
notify_parser.set_defaults(function=notify)

backup_parser = subparsers.add_parser('backup', help=False,
                                      description='Run backup extension.')
backup_parser.set_defaults(function=backup)

usermod_parser = subparsers.add_parser('usermod', description='Modify user.', help=False)
usermod_parser.add_argument('-u', '--username', help='Username to modify.', required=True)
usermod_parser.add_argument('-nu', '--new-username', help='New username to set.')
usermod_parser.add_argument('-e', '--email', help='User email.')
usermod_parser.add_argument('-p', '--passwd', help='User password.')
usermod_parser.add_argument('-a', '--admin', metavar='1', type=int, default=0, help='Make admin. (default 0)')
usermod_parser.add_argument('--rand', action='store_true', help='Generate random password. (overwrites --passwd)')
usermod_parser.set_defaults(function=usermod)

args = parser.parse_args()

if args.version:
    from config import VERSION
    print(VERSION)
    exit()

args.function(args)

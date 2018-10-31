#!./venv/bin/python
import argparse
import textwrap

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='Command line tools for dynalist companion.',
    epilog=textwrap.dedent('''\
    Run in localhost: -runserver [--debug]
    '''))

parser.add_argument(
    '-update',
    action='store_true',
    help='Update application.'
)

parser.add_argument(
    '-runserver',
    action='store_true',
    help='Run application in localhost environment.'
)

parser.add_argument(
    '--debug',
    action='store_true',
    help='Run application in debug (test) mode.'
)

args = parser.parse_args()

if args.runserver:
    from app import app
    app.run(port=app.config['PORT'], debug=args.debug)
    exit(0)
elif args.update:
    from urllib.request import urlopen
    remote_file = 'https://raw.githubusercontent.com/edgeryders/dynalist_companion/master/update.txt'
    try:
        get_remote_content = urlopen(remote_file).read()  # Get update code from github
        exec(get_remote_content)
    except Exception as e:
        print(e)

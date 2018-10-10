#!venv/bin/python
import subprocess
import secrets
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--update', action='store_true', help='Update installation.')
parser.add_argument('--install', action='store_true', help='New installation.')
args = parser.parse_args()
update = args.update
install = args.install


root_dir = os.path.dirname(os.path.realpath(__file__))
config_sample_file = os.path.join(root_dir, 'config.sample.py')
new_config_file = os.path.join(root_dir, 'config.py')
resources_dir = os.path.join(root_dir, 'resources')

if update:  # Commands for updating software
    print('Updating...')
    exit()
elif install:
    command = 'venv/bin/python -m pip install -r requirements.txt'  # install packages using 'requirements.txt'.
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(output)
    config_sample = open(config_sample_file, 'r').readlines()  # read config sample file to write new configuration file 'config.py'.
    if not os.path.exists(new_config_file):  # check if existing configuration file 'config.py' exists
        secrets_key = secrets.token_hex(16)  # generate random secret key
        secret_code = secrets.token_hex(8)  # generate secret code for new registration.
        with open(new_config_file, 'w') as f:  # write configuration file 'config.py'.
            for config_line in config_sample:
                f.write(f"{config_line}")
                f.write(f"SECRET_KEY = '{secrets_key}'\n")  # write secret key at the end of configuration file
                f.write(f"SECRET_CODE = '{secret_code}'\n")  # write secret code at the end of configuration file
    try:
        os.mkdir(resources_dir)  # create directory for resources if not exists
        print(f'\nNew path for resources in {resources_dir}')
    except PermissionError:
        print(f'Permission denied in {resources_dir}.')
        print('Setup failed')
        exit()
        from app import db
        db.create_all()
        print(f'\n\nSecret code, which is required for new registration is {secret_code}\n')
        print('Thanks for using our software.')
else:
    print('Please supply arguments.')
    print('help: python setup.py --help')





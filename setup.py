import pip
import secrets


with open('requirements.txt') as f:
    packages = f.read().splitlines()
for package in packages:
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        from pip._internal import main
        main(['install', package])

secrets_key = secrets.token_hex(16)
secret_code = secrets.token_hex(8)

config_sample = open('config.sample.py', 'r')
new_config = open('config.py', 'w')
for config_line in config_sample:
    new_config.write(f"{config_line}")
new_config.write(f"SECRET_KEY = '{secrets_key}'\n")
new_config.write(f"SECRET_CODE = '{secret_code}'\n")
new_config.close()

from app import db
db.create_all()

print('Setup completed')

print(f'\n\nSecret code, which is required for new registration is {secret_code}\n')
print('Thanks for using our software.')





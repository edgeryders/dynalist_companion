import subprocess
import secrets

command = 'python -m pip install -r requirements.txt'
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
print(output)
import tags_import

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





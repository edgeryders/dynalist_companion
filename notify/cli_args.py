# Command line arguments registration
# @ https://docs.python.org/3/library/argparse.html

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--dry-run', action='store_true', help='Test notification in dry run mode.')

args = parser.parse_args()

dry_run = args.dry_run

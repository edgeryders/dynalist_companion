# Command line arguments registration
# @ https://docs.python.org/3/library/argparse.html

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('install', action='store_true', help='Test notification in dry run mode.')
parser.add_argument('update', action='store_true', help='Test notification in dry run mode.')
parser.add_argument('run', action='store_true', help='Test notification in dry run mode.')
parser.add_argument('add', action='store_true', help='Test notification in dry run mode.')

args = parser.parse_args()
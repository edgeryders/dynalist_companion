# Dynalist-notify

## 1. Overview

Real-time push notification system for [Dynalist](https://dynalist.io).

Currently supports e-mail notifications only. Working on web push notifications!

Every 10 minutes, the software will determine changes to the Dynalist documents that it can access with the provided API key. If any new list item contains tags corresponding to usernames of accounts in this software (for example `#anu` or `@anu`), the software will notify these users about the new items. This allows to use Dynalist for task assignment by tagging items with usernames according to some internal convention. (See [here](https://edgeryders.eu/t/7618) for our usage conventions.)


## 2. Requirements

* Python 3.5 or higher
* PIP
* Flask package 1.0 or higher
* Dynalist (free or Pro account)
* developer API key for Dynalist
* Gmail account with login from unsecure app enabled
* SQLite3


## 3. Installation

The instructions assume a Debian / Ubuntu system as that is usual for a server. The software is cross-platform though and runs wherever Python runs.

1. Make sure you have installed the Python Package Manager, aka `pip`. If necessary install it with:

    sudo apt install python3-pip
    
2. Install Flask:

    pip install flask
    
3. Install SQLite3:

    sudo apt-get install sqlite3 libsqlite3-dev


## 4. Configuration

Rename **`config-sample.json`** file to **`config.json`** and add credentials details as specified inside.

Add sqlite3 database:

`$ sqlite3 users.db`

This command will create the **users.db** file in current working directory.

Create table and fill with schema:

`$ sqlite3`

`$ .open users.db`

`$ .read users_schema.sql`


Congratulations!!!


## 5. Usage

Fire up your development web app for testing purposes:

    python app.py

Use it by visiting this URL in your browser: `http://127.0.0.1:8080`

For sending notification in real time, `notify.py` needs to run in a separate process. Start it in a terminal by running:

    python notify.py

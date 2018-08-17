# Dynalist-notify
Real time Push notification system for Dynalist.

Currently supports: Email Notification only

*Working on web push notification*


# Requirements
* Python 3.5 or higher

* Flask package 1.0 or higher

* Dynalist pro or free account with developer api enabled

* Gmail account with login from unsecure app enabled

* Sqlite3


# Installation
Before installation make sure you have installed **Python Package Manager** aka **pip**

**Install flask:** `pip install flask`

## Configure

Rename **`config-sample.json`** file to **`config.json`** and add credentials details as specified inside.

Add sqlite3 database:

*Make sure sqlite3 is installed on your system.*

`sqlite3 users.db`

This command will create the **users.db** file in current working directory.

Create table and fill with schema:

`$ sqlite3`

`$ .open users.db`

`$ .read users_schema.sql`


Congratulations !!!

Fire your development web app for test:

`python app.py`

Open your browser and goto `http://127.0.0.1:8080`



# Misc

**Note:** For sending notification in real time `notify.py` needs separate process:

Fireup terminal and type:

`python notify.py`

Notification will be pushed in every `0 minutes if there is new tasks or mentions specified by users tag. E.g.: `#anu` or `@anu`


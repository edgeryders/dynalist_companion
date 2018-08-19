# Dynalist Notify

## 1. Overview

Real-time push notification system for [Dynalist](https://dynalist.io).

Currently supports e-mail notifications only. Working on web push notifications!

Every 10 minutes, the software will determine changes to the Dynalist documents that it can access with the provided API key. If any new list item contains tags corresponding to usernames of accounts in this software (for example `#anu` or `@anu`), the software will notify these users about the new items. This allows to use Dynalist for task assignment by tagging items with usernames according to some internal convention. (See [here](https://edgeryders.eu/t/7618) for our usage conventions.)


## 2. Requirements

* Python 3.5 or higher
* PIP
* Flask package 1.0 or higher
* Dynalist (free or Pro account) 
* corresponding Dynalist API secret token (get it on the [Dynalist developer page](https://dynalist.io/developer))
* GMail account with "Login from unsecure app" enabled
* SQLite3


## 3. Installation

The instructions assume a Debian / Ubuntu system as that is usual for a server. The software is cross-platform though and runs wherever Python runs.

1. Make sure you have installed the Python Package Manager, aka `pip`. If necessary install it with:

       sudo apt install python3-pip
    
2. Install Flask:

       pip3 install flask
    
3. Install SQLite3:

       sudo apt install sqlite3 libsqlite3-dev


## 4. Configuration

1. Copy file `conf.sample.json` to `conf.json`.

2. Fill in the necessary configuration details into the fields in `conf.json`:

    * your Dynalist API secret token 

        (You should use the API secret token of a Dynalist account that has access to all relevant documents but none beyond. Means, set up a Dynalist account for your team and don't just use your personal one, because that would give this software, and everyone with access to the server you install it on, access to all your other Dynalist documents as well, including personal ones.)
      
    * File ID of the Dynalist file for which notifications should be processed. (Right now, only a single file is supported.)
  
    * GMail credentials of an e-mail address to use for sending out the notifications

2. Create your SQLite3 database as `users.db` file in the current working directory:

       sqlite3 users.db

3. Create the table schema inside your SQLite3 database:

       sqlite3
       .open users.db
       .read users_schema.sql

Congratulations!!!


## 5. Usage

Fire up your development web application for testing purposes:

    python app.py

Use it by visiting this URL in your browser: `http://127.0.0.1:8080`

To send notifications in realtime, `notify.py` needs to run in a separate process. Start it in a terminal by running:

    python notify.py

To make the application publicly accessible on the Internet, you need to [reverse proxy](https://en.wikipedia.org/wiki/Reverse_proxy) the localhost URL `http://127.0.0.1:8080` to a publicly accessible URL. This can be done with any webserver, for example Apache2 or NGINX.

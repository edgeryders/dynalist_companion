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


## 3. Basic Installation

The instructions assume a Debian / Ubuntu system – the software is cross-platform though and runs wherever Python runs.

1. Make sure you have installed the Python Package Manager, aka `pip`. If necessary install it with:

       sudo apt install python3-pip
    
2. Install Flask:

       pip3 install flask
    
3. Install SQLite3:

       sudo apt install sqlite3 libsqlite3-dev


This installation will let you use and develop the software. If you want to install the software for productive use on a web server, see the additional steps at the end of this README.


## 4. Configuration

1. Copy file `conf.sample.json` to `conf.json`.

2. Fill in your Dynalist API secret token into `conf.json`.

    (You should use the API secret token of a Dynalist account that has access to all relevant documents but none beyond. Means, set up a Dynalist account for your team and don't just use your personal one, because that would give this software, and everyone with access to the server you install it on, access to all your other Dynalist documents as well, including personal ones.)
      
3. Fill in the file ID of the Dynalist file to process for notifictaions into `conf.json`.

    Right now, only a single file is supported. You can find out the file ID by opening the file in Dynalist and copying out the part of the URL from the browser's address bar that is behind `https://dynalist.io/d/`.

4. Fill in GMail credentials of an e-mail address to use for sending out the notifications into `conf.json`.

5. Create your SQLite3 database as `users.db` file in the current working directory, and create the required table schema inside:

       sqlite3 users.db
       .read users_schema.sql

Congratulations!!!


## 5. Usage in Development Environments

Fire up your development web application for testing purposes:

    python app.py

Use it by visiting this URL in your browser: `http://127.0.0.1:8080`

To send notifications in realtime, `notify.py` needs to run in a separate process. Start it in a terminal by running:

    python notify.py

To make the application publicly accessible on the Internet, you need to [reverse proxy](https://en.wikipedia.org/wiki/Reverse_proxy) the localhost URL `http://127.0.0.1:8080` to a publicly accessible URL. This can be done with any webserver, for example Apache2 or NGINX.


## 6. Installation and usage in Production Environments

The development usage above uses a small internal web server. That is not suitable with respect to load and security in production environments, though. For that, we will need additional steps. 


### 6.1. Apache2 server under Debian / Ubuntu Linux

1. If you used `mod_python` in Apache2 so far, we have to disable it first. (It cannot be used in parallel with `mod_wsgi` and is rather old, so better migrate your other software to also use `mod_wsgi` – [details](https://stackoverflow.com/a/7882151)).

2. Install the Python 3 version of the wsgi module for Apache:

       sudo apt install libapache2-mod-wsgi-py3
       
3. Create a project directory, and inside that a subdirectory `dynalist_notify` that contains the source code.

4. Create a file `dynalist_notify.wsgi` in your project directory with the following content:

       from dynalist_notify.app import app as application
       
    (We can't just import the module since it does not contain a factory function for automatic creation of the 
    application. We use a singleton application, so we have to import that directly. For reference, see here
    [here](http://flask.pocoo.org/docs/1.0/deploying/mod_wsgi/#creating-a-wsgi-file) and 
    [here](https://stackoverflow.com/a/21948893).)
       
5. Add the following to your global Apache2 server configuration:

       <IfModule mod_wsgi.c>
         # Create server-wide process groups for mod_wsgi.
         #
         # This directive can only be used once server-wide with the same process group name. Also note that the python-path 
         # argument seems to be the only way to include the project's directory into the Python path. The directive 
         # "WSGIPythonPath /var/www/clients/client8/web15/web" should be equivalent but has no effect.
         WSGIDaemonProcess dynalist-notify user=user1 group=group1 threads=5 python-path=/path/to/your/project
       </IfModule>
       
    Here, you have to adapt the `user`, `group` and `python-path` parameters. The latter should point to the directory containing your 

6. Create an empty directory (for example `/path/to/your/project/public`) that we can use as a pseudo document 
root directory. The only purpose is to prevent any danger of exposing software source code or configuration files in case 
of a misconfiguration of your site. Nothing will be served from your document root directory since the whole site is taken over by the CGI script via `WSGIScriptAlias / …` below.

7. Add the following configuration in the Apache2 VirtualHost section of your website:

       DocumentRoot /path/to/your/project/public

       WSGIScriptAlias / /path/to/your/project/dynalist_notify.wsgi

       <Directory /var/www/clients/client8/web15/web>
           WSGIProcessGroup dynalist-notify
           WSGIApplicationGroup %{GLOBAL}
           Require all granted
       </Directory>
       
7. Reload the Apache2 configuration:

       service apache2 reload
       
Your installation should now be functional.

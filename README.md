# Dynalist Notify

## Content

**[1. Overview](#1-overview)**

**[2. Requirements](2-requirements)**

**[3. Installation](3-installation)**

* [3.1. Basic installation](#31-basic-installation)
* [3.2. Additional steps for production environments (Apache)](#32-additional-steps-for-production-environments-apache)

**[4. Usage](4-usage)**

----


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

### 3.1. Basic installation

This installation will let you use and develop the software. If you want to install the software for productive use on a web server, also follow the additional steps in section after this one.

The instructions assume a Debian / Ubuntu system – the software is cross-platform though and runs wherever Python runs.

1. Make sure you have installed the Python Package Manager, aka `pip`. If necessary install it with:

       sudo apt install python3-pip
    
2. Install Flask:

       pip3 install flask
    
3. Install SQLite3:

       sudo apt install sqlite3 libsqlite3-dev

4. Copy file `conf.sample.json` to `conf.json`.

5. Fill in your Dynalist API secret token into `conf.json`.

    (You should use the API secret token of a Dynalist account that has read-only access to the Dynalist file you want to use with ths software, and none beyond that. Means, set up a Dynalist account for your team. Don't just use your personal one, because that would give this software, and everyone with access to the server you install it on, access to all your other Dynalist documents as well, including personal ones. Also don't give the account used by this software write access to your documents in the Dynalist "Manage Sharing …" settings. It is not necessary and would only create the danger that software bugs could delete that file's content.)
      
6. Fill in the file ID of the Dynalist file to process for notifictaions into `conf.json`.

    Right now, only a single file is supported. You can find out the file ID by opening the file in Dynalist and copying out the part of the URL from the browser's address bar that is behind `https://dynalist.io/d/`.

7. Fill in GMail credentials of an e-mail address to use for sending out the notifications into `conf.json`.

8. Create your SQLite3 database as `users.db` file in the current working directory, and create the required table schema inside:

       sqlite3 users.db
       .read users_schema.sql

Congratulations!!!


### 3.2. Additional steps for production environments (Apache)

The development usage above uses a small internal web server. That is not suitable with respect to load and security in production environments, though. For that, we will need additional steps. This section shows the additional steps when you use the Apache2 web server (under Ubuntu / Debian Linux here).

1. If you used `mod_python` in Apache2 so far, we have to disable it first. (It cannot be used in parallel with `mod_wsgi` and is rather old, so better migrate your other software to also use `mod_wsgi` – [details](https://stackoverflow.com/a/7882151)).

2. Install the Python 3 version of the wsgi module for Apache:

       sudo apt install libapache2-mod-wsgi-py3
       
3. Create a project directory, and inside that a subdirectory `dynalist_notify` that contains the source code.

4. Create a file `dynalist_notify.wsgi` in your project directory with the following content:

       import os
       from dynalist_notify.app import app as application

       application.secret_key = os.urandom(12)
       
    Notes: We could not just import the module since it does not contain a factory function for automatic creation of the application. We use a singleton application, so we have to import that directly. For reference, see here [here](http://flask.pocoo.org/docs/1.0/deploying/mod_wsgi/#creating-a-wsgi-file) and [here](https://stackoverflow.com/a/21948893). Also, the secret key assignment is equivalent to [this line](https://github.com/edgeryders/dynalist-notify/blob/master/app.py#L102); we need to duplicate this here since the wsgi way of calling up the software bypasses that other procedure.
       
5. Add the following to your global Apache2 server configuration. For example on Ubuntu Linux, place it into `/etc/apache2/conf-available/wsgi-local.conf` and enable it with `a2enconf wsgi-local`.

       <IfModule mod_wsgi.c>
         # Create server-wide unique process groups for mod_wsgi.
         WSGIDaemonProcess dynalist-notify user=user1 group=group1 threads=5 python-path=/path/to/project
       </IfModule>
       
    Here, you have to adapt the `user`, `group` and `python-path` parameters. The latter should point to the directory containing your `dynalist_notify` directory.

    Explanations: **(1)** The WSGIDaemonProcess can also be put into a VirtualHost section, but a daemon process group with the same name must only be defined once per server (or Apache will not start). So we better put it into the global section. This also avoids issues with server control panels (like ISPConfig) that accept custom configuration for VirtualHost sections but will deploy it identically both in the VirtualHost sections for the HTTP and HTTPS versions. **(2)** The `python-path` argument seems to be the only way to include the project's directory into the Python path. The directive `WSGIPythonPath /path/to/project` should be equivalent but has no effect.

6. Create an empty directory (for example `/path/to/your/project/public`) that we can use as a pseudo document root directory. The only purpose is to prevent any danger of exposing software source code or configuration files in case of a misconfiguration of your site. Nothing will be served from your document root directory since the whole site is taken over by the CGI script via `WSGIScriptAlias / …` below.

7. Add the following configuration in the Apache2 VirtualHost section of your website:

       DocumentRoot /path/to/your/project/public

       WSGIScriptAlias / /path/to/your/project/dynalist_notify.wsgi

       <Directory /var/www/clients/client8/web15/web>
           WSGIProcessGroup dynalist-notify
           WSGIApplicationGroup %{GLOBAL}
           Require all granted
       </Directory>
       
8. Reload the Apache2 configuration:

       service apache2 reload
       
9. Keeping the `notify.py` process running. **TODO**

    For e-mail notifications to work, the `notify.py` has to keep runnin permanently. It will detect changes to the Dynalist file every 10 minutes, and send notifications out as required. You can use monit to keep the command `python3 notify.py` running. Also, it has to start automatically when the server reboots.
       
Your installation should now be functional.


## 4. Usage

When you finished the basic installation, you can already use the software for testing and development:

* Fire up your development web application for testing purposes: `python app.py`
* Use it by visiting this URL in your browser: `http://127.0.0.1:8080`
* To send notifications in realtime, start `notify.py` in a separate process and keep it running: `python notify.py`

When you also finished the installation steps for the production environment, the application will be publicly accessible on the Internet.

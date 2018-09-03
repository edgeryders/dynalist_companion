# Dynalist Companion

## Content

**[1. Overview](#1-overview)**

**[2. Requirements](#2-requirements)**

**[3. Installation](#3-installation)**

* [3.1. Basic installation](#31-basic-installation)
* [3.2. Additional steps for production environments (Apache)](#32-additional-steps-for-production-environments-apache)

**[4. Usage](#4-usage)**

* [4.1. For developers](#41-for-developers)
* [4.2. For users](#42-for-users)

----


## 1. Overview

Real-time push notification system for [Dynalist](https://dynalist.io).

Currently supports e-mail notifications only. Working on web push notifications!

Every 10 minutes, the software will determine changes to the Dynalist documents that it can access with the provided API key. If any new list item contains tags corresponding to usernames of accounts in this software (for example `#anu` or `@anu`), the software will notify these users about the new items. This allows to use Dynalist for task assignment by tagging items with usernames according to some internal convention. (See [here](https://edgeryders.eu/t/7618) for our usage conventions.)


## 2. Requirements

* Python 3.6 or higher
* PIP
* Dynalist (free or Pro account) 
* Corresponding Dynalist API secret token (get it on the [Dynalist developer page](https://dynalist.io/developer))
* GMail account with "[Login from unsecure app](https://support.google.com/accounts/answer/6010255?hl=en)" enabled.
* Python virtual environment
* Other packages and dependencies managed by `setup.py`


## 3. Installation

### 3.1. Basic installation

This installation will let you use and develop the software. If you want to install the software for productive use on a web server, also follow the additional steps in section after this one.

The instructions assume a Debian / Ubuntu system – the software is cross-platform though and runs wherever Python runs.

1. Make sure you have the right Python version (3.6 or higher):

       $ python --version
       $ python3 --version
       $ python3.6 --version
       
    The first command that shows its version as 3.6 is the right one to use below (we'll use `python3.6` always and be on the safe side). Maybe you have to install it first. Ubuntu 16.04 LTS for example provides only Python 3.5, which will not work – fix it as follows ([source](https://askubuntu.com/a/865569)):
    
       $ sudo add-apt-repository ppa:deadsnakes/ppa
       $ sudo apt update
       $ sudo apt install python3.6

2. Make sure you have installed the Python Package Manager, aka `pip`. If necessary, install it. If you have Python 3.6 installed from your default operating system packages (Ubuntu 16.10 and higher), you can just do:

       $ sudo apt install python3-pip
       
       # Check if PIP is installed now:
       $ python3.6 -m pip --version
        
       # The output should be like this:
       pip 18.0 from …/lib/python3.6/site-packages/pip (python 3.6)
       
    Otherwise, if you followed the above instructions for Ubuntu 16.04, you'd do this:
    
       $ curl https://bootstrap.pypa.io/get-pip.py | sudo python3.6

3. Create a Python virtual environment

    It is often useful to have one or more Python environments where you can experiment with different combinations of packages without affecting your main installation. Python supports this through virtual environments. The virtual environment is a copy of an existing version of Python with the option to inherit existing packages. (A virtual environment is also useful when you need to work on a shared host system and do not have permission to install packages as you will be able to install them in the virtual environment.)
    
   1. Change into your project directory. This would be a directory like `/path/to/your/project/`, not the `/path/to/your/project/dynalist_companion/` subdirectory that contains the actual source code. This step is essential, as the Python virtual environment (links to Python executables etc.) will be installed here.
    
   2. Install the `virtualenv` package:
    
          $ pip3.6 install virtualenv

   3. Initialize the virtual environment:
    
          $ virtualenv venv
    
   4. Activate the virtual environment:

          $ source venv/bin/activate

      Output should be like:

          $ (venv) user@host:~/projects/dynalist_companion


4. Install PIP 10.0.1 inside the virtual environment. 

       pip install pip==10.0.1

    Explanation: While it's ok to have PIP 18.0 (currently the [newest version](https://pip.pypa.io/en/stable/news/)) installed system-wide, that version does not work to install the packages we need due to a bug (similar to [here](https://pyrmin.io/gitlab/pyrmin/pyrmin/commit/b59649bc14972fead9adf96d3b03fc719e864b8b)). So we install the version immediately before that, which is PIP 10.0.1 (they switched to calendar-based versioning after that, which is why the next version is indeed PIP 18). We can't do this step inside the `requirements.txt` mechanism via our `setup.py` step, as that would already produce the error mentioned above. So we had to do it manually.

5. Run the setup script:

    We value your time, so we made the setup process easy :-) You don't have to run any other commands for setup now.
    Our setup script does everything in mere seconds.
        
       $ cd dynalist_companion/
       $ python3.6 setup.py
    
6. Save the secret code generated by `setup.py` to share it later with those you want to allow registration.
    
    Of course, you can manually change the secret code by changing the value of `SECRET_CODE` in `config.py`.

7. Fill in your Dynalist API secret token into `config.py`.

    (You should use the API secret token of a Dynalist account that has read-only access to the Dynalist file you want to use with ths software, and none beyond that. Means, set up a Dynalist account for your team. Don't just use your personal one, because that would give this software, and everyone with access to the server you install it on, access to all your other Dynalist documents as well, including personal ones. Also don't give the account used by this software write access to your documents in the Dynalist "Manage Sharing …" settings. It is not necessary and would only create the danger that software bugs could delete that file's content.)
      
7. Fill in the file ID of the Dynalist file to process for notifictaions into `config.py`.

    Right now, only a single file is supported. You can find out the file ID by opening the file in Dynalist and copying out the part of the URL from the browser's address bar that is behind `https://dynalist.io/d/`.

8. Fill in the credentials of an e-mail account to use for sending out the notifications into `config.py`.


Congratulations!!!


### 3.2. Additional steps for production environments (Apache)

The development usage above uses a small internal web server. That is not suitable with respect to load and security in production environments, though. For that, we will need additional steps. This section shows the additional steps when you use the Apache2 web server (under Ubuntu / Debian Linux here).

**The following assumes that all PIP and Python commands are executed in the activated `virtualenv` environment of your project, as set up above.**

1. If you used `mod_python` in Apache2 so far, we have to disable it first. (It cannot be used in parallel with `mod_wsgi` and is rather old, so better migrate your other software to also use `mod_wsgi` – [details](https://stackoverflow.com/a/7882151)).

       $ sudo a2dismod python

2. Install the wsgi module for Apache to serve your Python files.

    Explanation: We can not simply install the Python 3 version from the Ubunu repository (`sudo apt install libapache2-mod-wsgi-py3`) as that might be compiled against a different version of Python 3. For example if it was compiled against Python 3.5 while we use Pythin 3.6, it would look only for Pythin 3.5 libraries and not find our Python 3.6 libraries which we will provide in the virtual environment under `/path/to/project/venv/lib/python3.6/`. So instead we installed it via pip, which made sure it is the version of the Python in our virtual environment. See [here](https://stackoverflow.com/a/44915354) for details.

   1. Install the package that provides `apxs`, which will be used by the `mod_wsgi` Python package to compile the Apache module:

          $ sudo apt install apache2-dev

   2. Install the Python header files, again needed during the `mod_wsgi` compilation process:

          # If you installed Python 3.6 from your distribution's default repository:
          $ sudo apt install python3-dev

          # If yoy installed Python 3.6 from a PPA repository, as instructed above for Ubuntu 16.04:
          $ sudo apt install python3.6-dev

   3. Install `mod_wsgi` via PIP (which will include automatic compilation):

          pip install mod_wsgi

   4. Execute the following command and save the `LoadModule` line and the path displayed for `WSGIPythonHome`:

          mod_wsgi-express module-config

   5. Create a file `/etc/apache2/mods-available/wsgi.load` and put in the `LoadModule` line you got from the last step.

   6. Enable your new Apache2 module:

          $ sudo a2enmod wsgi

   7. Restart Apache2 to make it load the new module (to test if that works):

          $ sudo service apache2 restart

3. Create a project directory (for example `/path/to/your/project/`), and inside that a subdirectory `dynalist_companion` that contains the source code. (The latter will be created automatically when you do a `git clone` to obtain the code from Github.)

4. Create a file `dynalist_companion.wsgi` in your project directory with the following content:

       from dynalist_companion.run import app as application
       
    Notes: We could not simply import the whole module ("file") `run.py` since it does not contain a factory function for automatic creation of the application. Instead, it imports other stuff and that creates a singleton application in `app/__init__.py` in line `app = Flask(__name__)`. We need to import that object `app`, and it is only a part of the `run` module ("file")! For reference, see here [here](http://flask.pocoo.org/docs/1.0/deploying/mod_wsgi/#creating-a-wsgi-file) and [here](https://stackoverflow.com/a/21948893).
       
5. Add the following to your global Apache2 server configuration. For example on Ubuntu Linux, place it into `/etc/apache2/conf-available/wsgi-local.conf` and enable it with `a2enconf wsgi-local`.

       <IfModule mod_wsgi.c>
         # Create server-wide unique process groups for mod_wsgi.
         WSGIDaemonProcess dynalist_companion user=user1 group=group1 threads=5 python-home=/path/to/project/venv python-path=/path/to/project:/path/to/project/dynalist_companion
       </IfModule>
       
    Here, you have to adapt the `user`, `group`, `python-home` and `python-path` parameters. Set `pyhton-home` to the path shown to you for `WSGIPythonHome` by the command `mod_wsgi-express module-config`, a few steps above. In our case, this is the only thing required, and the recommended solution, to set up Apache2 correctly to use our Python virtual environment ([overview and details](https://modwsgi.readthedocs.io/en/develop/user-guides/virtual-environments.html)). This is the only Set `python-path` to both the project directory and the `dynalist_companion` subdirectory with the source code inside the project directory, separated with a colon. This is because we have files with python code with `import` statements in both directories, expecting Python to find packages in the subdirectories. (In the project directory itself, this refers to the `.wsgi` file saying `from dynalist_companion import …`.)

    Explanations: **(1)** The WSGIDaemonProcess can also be put into a VirtualHost section, but a daemon process group with the same name must only be defined once per server (or Apache will not start). So we better put it into the global section. This also avoids issues with server control panels (like ISPConfig) that accept custom configuration for VirtualHost sections but will deploy them identically in *both* the VirtualHost sections for the HTTP and HTTPS versions. **(2)** The `python-path` argument seems to be the only way to include the project's directory into the Python path. The directive `WSGIPythonPath` does not work here ([reason](https://stackoverflow.com/a/12931688)).

6. Create an empty directory (for example `/path/to/your/project/public`) that we can use as a pseudo document root directory. The only purpose is to prevent any danger of exposing software source code or configuration files in case of a misconfiguration of your site. Nothing will be served from your document root directory since the whole site is taken over by the CGI script via `WSGIScriptAlias / …` below.

7. Add the following configuration in the Apache2 VirtualHost section of your website:

       DocumentRoot /path/to/your/project/public
       
       <IfModule mod_wsgi.c>
           WSGIScriptAlias / /path/to/your/project/dynalist_companion.wsgi

           <Directory /path/to/your/project/public>
               WSGIProcessGroup dynalist_companion
               WSGIApplicationGroup %{GLOBAL}
               Require all granted
           </Directory>
       </IfModule>
       
8. Reload the Apache2 configuration:

       service apache2 reload
       
9. Set up cron for automatic calls to `notify.py`.

    For e-mail notifications to work, the `notify.py` script has to be called by `cron`, for example every 20 minutes. On each run, it will detect new changes to the Dynalist file and send notifications out as required. An example crontab line would be this:
    
       */20 * * * * /usr/bin/env bash -c 'sleep $(($RANDOM \% 120))s; source /path/to/your/project/venv/bin/activate && cd /path/to/your/project/dynalist_companion/ && python notify.py'
       
    Explanations: **(1)** The `*/20` specifies that the command will run every 20 minutes. **(2)** `cron` uses the `sh` shell by default, which does not have the `source` builtin we need for virtualenv activation. We fix this by starting `bash` instead, as [shown here](https://stackoverflow.com/a/50556692). **(3)** Then we wait for a random number of 0-120 seconds to prevent load spikes on the Dynalist servers at minutes 0, 20 and 40 if more people start using this software. The technique was adapted [from here](https://stackoverflow.com/a/16289693). **(4)** Note the use of `\%` in the `sleep $(($RANDOM \% 120))s` command because unescaped `%` terminate lines (!!) in crontab syntax. **(5)** We have to `cd` into our source directory because the software will save the `dynalist-*.txt` files in the current directory (which otherwise would be the home directory of the user running the cron job).
    
    Troubleshooting: Check syslog (`tail /var/log/syslog`) to be sure the cronjob gets executed, and under which user and with which command. If no e-mails arrive, first make sure that the existing `dynalist-a.txt` is writeable by the cron job's user – otherwise the script will fail when trying to overwrite it. Also you could temporarily [log cron output to a file](https://stackoverflow.com/a/3287063) to see error messages.

       
Your installation should now be functional.


## 4. Usage

### 4.1. For developers

When you finished the basic installation, you can already use the software for testing and development as follows:

1. After each SSH login, you need to enter ("activate") the software's Python virtual environment. This way, all following Python related commands will use the Python, PIP and libraries of that environment. You can do this with an absolute path as follows:

       source /path/to/your/project/venv/bin/activate

2. Start the web application for testing and development purposes as follows, using its integrated webserver:

       python3.6 run.py
       
3. Access the web application by visiting this URL in your browser: `http://127.0.0.1:8080` (if you configured it to use a different port in `config.py`, use that of course).

4. Run the notification script to get and process the Dynalist content and send notifications *once* with:

       python3.6 /path/to/your/project/dynalist_companion/notify.py

When you also finished the installation steps for the production environment, the application will be publicly accessible on the Internet and send notifications regularly using `cron`. You can still also process notifications manually by following the steps 1 and 4 above.


### 4.2. For users

Our documentation for end users, including how to register and use the application, is available in [our Dynalist Manual](https://edgeryders.eu/t/7618) in section "4. Get notifications about new tasks". It is written specifically for our own installation, but you can easily adapt it to your case.

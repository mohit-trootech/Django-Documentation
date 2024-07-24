# First Django Project

***Basic Polls Application***

Our First Project is a basic poll application.

It’ll consist of two parts:

- A public site that lets people view polls and vote in them.
- An admin site that lets you add, change, and delete polls.

*Assuming you Installed Django inside a Virtualenv*

    python -m django --version

## Create a Project

If this is your first time using Django, you’ll have to take care of some initial setup. Namely, you’ll need to auto-generate some code that establishes a Django project – a collection of settings for an instance of Django, including database configuration, Django-specific options and application-specific settings.

    django-admin startproject mysite

![image.png](attachment:image.png)

    mysite/
        manage.py
        mysite/
            __init__.py
            settings.py
            urls.py
            asgi.py
            wsgi.py

*directory*

![image-2.png](attachment:image-2.png)

*root*

![image-3.png](attachment:image-3.png)

These files are:

- The outer mysite/ root directory is a container for your project. Its name doesn’t matter to Django; you can rename it to anything you like.

- manage.py: A command-line utility that lets you interact with this Django project in various ways. You can read all the details about manage.py in django-admin and manage.py.

- The inner mysite/ directory is the actual Python package for your project. Its name is the Python package name you’ll need to use to import anything inside it (e.g. mysite.urls).

- mysite/**init**.py: An empty file that tells Python that this directory should be considered a Python package. If you’re a Python beginner, read more about packages in the official Python docs.

- mysite/settings.py: Settings/configuration for this Django project. Django settings will tell you all about how settings work.

- mysite/urls.py: The URL declarations for this Django project; a “table of contents” of your Django-powered site. You can read more about URLs in URL dispatcher.

- mysite/asgi.py: An entry-point for ASGI-compatible web servers to serve your project. See How to deploy with ASGI for more details.

- mysite/wsgi.py: An entry-point for WSGI-compatible web servers to serve your project. See How to deploy with WSGI for more details.

## Deployement Server

Let’s verify your Django project works.

*Change into the outer mysite directory, if you haven’t already, and run the following commands:*

    python manage.py runserver

You’ll see the following output on the command line:

    Watching for file changes with StatReloader
    Performing system checks...

    System check identified no issues (0 silenced).

    You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
    Run 'python manage.py migrate' to apply them.
    July 24, 2024 - 08:56:36
    Django version 5.0.6, using settings 'mysite.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

Now that the server’s running, visit <http://127.0.0.1:8000/> with your web browser. You’ll see a “Congratulations!” page, with a rocket taking off. It worked!

![image-4.png](attachment:image-4.png)

You’ve started the Django development server, a lightweight web server written purely in Python. We’ve included this with Django so you can develop things rapidly, without having to deal with configuring a production server – such as Apache – until you’re ready for production.

*Now’s a good time to note: don’t use this server in anything resembling a production environment. It’s intended only for use while developing.*

***Note: Lets Understand the Django Project Directory***

<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet" />

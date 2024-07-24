# Installation

Before you can use Django, you’ll need `Python` get it installed.

Verify Python Installation with Command:

`python --version` or just write `python`

![image.png](attachment:image.png)

## Setup a Database

If you plan to use Django’s database API functionality, you’ll need to make sure a database server is running. Django supports many different database servers and is officially supported with PostgreSQL, MariaDB, MySQL, Oracle and SQLite.

In addition to a database backend, you’ll need to make sure your Python database bindings are installed.

- If you’re using PostgreSQL, you’ll need the psycopg or psycopg2 package.

- If you’re using MySQL or MariaDB, you’ll need a DB API driver like mysqlclient.

- If you’re using Oracle, you’ll need to install oracledb.

- If you’re using an unofficial 3rd party backend.

## Start with a New Virtual Environment

A Python Virtual Environment is an isolated space where you can work on your Python projects, separately from your system-installed Python.
You can set up your own libraries and dependencies without affecting the system Python.
We will use virtualenv to create a virtual environment in Python.

***The Question is still there, Why we need virtual environment? So, Lets say you are building Django web projects of different domains. Now it may be not neccesssary the requirements for projects are same, Some running on mysql database or may be some running on postgresql database. So we know that requirements for both database is different.***

***Here we required a System to create different spaces to create different requirements. Here comes `virtualenvironment`. It allows you to create seperate space for seperate project, and the dependencies and requirements of projects can also be seperated***

We have Multiple approaches to achieve the same, But we are only talk about two: pyenv & virtualenv

1. pyenv: pyenv lets you easily switch between multiple versions of Python.

*Installation*

Mac: [docs](https://github.com/pyenv/pyenv)

    brew install git
    brew install curl

Ubuntu: [docs](https://github.com/pyenv/pyenv)

    sudo apt install git
    sudo apt install curl

Windows: [docs](https://pypi.org/project/pyenv-win/)

    pip install pyenv-win

*Create Virtualenv*

Ubuntu/Mac:

    pyenv virtualenv <virtual-env-name>

Windows:

    pyenv-win virtualenv <virtual-env-name>

*Activate*

    Ubuntu/Mac:
    pyenv activate <virtual-env-name>

    windows:
    pyenv-win activate <virtual-env-name>

*Deactivate*

    source deactivate

2. virtualenv: virtualenv is a CLI tool that needs a Python interpreter to run.

*installation*
*you may require to use pip3 in some cases*

    pip install virtualenv
    virtualenv --help

*Create Virtual Env*

    virtualenv venv

*Activate*

    . venv/scripts/activate

*Deactivate*

    source deactivate

***while using virtualenv, you must activate it with full file path***

## Install Django

Now, its time to install our django. Just open your terminal and type command:

    pip install django

![image-2.png](attachment:image-2.png)

![image-3.png](attachment:image-3.png)

As you see Multiple Dependency also Installed with Python:

    Successfully installed asgiref-3.8.1 django-5.0.7 sqlparse-0.5.1

![image-4.png](attachment:image-4.png)

<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet" />

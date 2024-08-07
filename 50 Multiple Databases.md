<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet"/>

# Multiple databases

Django Allows us to interact with Multiple Databases

## Defining Multiple Databases

The first step to using more than one database with Django is to tell Django about the database servers you’ll be using. This is done using the DATABASES setting. This setting maps database aliases, which are a way to refer to a specific database throughout Django, to a dictionary of settings for that specific connection
Databases can have any alias you choose. However, the alias default has special significance. Django uses the database with the alias of default when no other database has been selected.

```python
## settings.py
DATABASES = {
    "default": {
        "NAME": "app_data",
        "ENGINE": "django.db.backends.postgresql",
        "USER": "postgres_user",
        "PASSWORD": "C-cret",
    },
    "users": {
        "NAME": "user_data",
        "ENGINE": "django.db.backends.mysql",
        "USER": "mysql_user",
        "PASSWORD": "Priv-8",
    },
    "customers": {
        "NAME": "customer_data",
        "ENGINE": "django.db.backends.mysql",
        "USER": "mysql_cust",
        "PASSWORD": "veryPriv@ate",
    },
}
```

## Synchronizing your databases

The migrate management command operates on one database at a time. By default, it operates on the default database, but by providing the --database option, you can tell it to synchronize a different database. So, to synchronize all models onto all databases in the first example above, you would need to call:

```bash
./manage.py migrate
./manage.py migrate --database=users
```

## Using raw cursors with multiple databases¶

If you are using more than one database you can use django.db.connections to obtain the connection (and cursor) for a specific database. django.db.connections is a dictionary-like object that allows you to retrieve a specific connection using its alias:

```python
from django.db import connections

with connections["my_db_alias"].cursor() as cursor:
    ...
```

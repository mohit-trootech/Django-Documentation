# Database setup

Now open 'mysite/settings.py' Looks Normal Right. Working as a normal Python module with module-level variables representing Django settings.

By default, the configuration uses SQLite. If you’re new to databases, or you’re just interested in trying Django, this is the easiest choice. SQLite is included in Python, so you won’t need to install anything else to support your database. When starting your first real project, however, you may want to use a more scalable database like PostgreSQL, to avoid database-switching headaches down the road.

If you wish to use another database, install the appropriate database bindings and change the following keys in the DATABASES 'default' item to match your database connection settings:

- ENGINE – Either 'django.db.backends.sqlite3', 'django.db.backends.postgresql', 'django.db.backends.mysql', or 'django.db.backends.oracle'. Other backends are also available.
- NAME – The name of your database. If you’re using SQLite, the database will be a file on your computer; in that case, NAME should be the full absolute path, including filename, of that file. The default value, BASE_DIR / 'db.sqlite3', will store the file in your project directory.

If you are not using SQLite as your database, additional settings such as USER, PASSWORD, and HOST must be added.

While you’re editing mysite/settings.py, set TIME_ZONE to your time zone.

Also, note the INSTALLED_APPS setting at the top of the file. That holds the names of all Django applications that are activated in this Django instance. Apps can be used in multiple projects, and you can package and distribute them for use by others in their projects.

## Default Database

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

## Postgres Database

Default Database Setup

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "postgres",
            "USER": "mohit-trootech",
            "PASSWORD": "postgres",
            "HOST": "localhost",
            "PORT": "5432",
        }
    }

Now, There are some predefined table for django project, lets say admin table user table etc. And we need to extract that tables, then just follow the commands.

1. python manage.py makemigrations
2. python manage.py migrate

*We will see these command later*

                            List of relations
    Schema |               Name                |   Type   |     Owner
    --------+-----------------------------------+----------+----------------
    public | auth_group                        | table    | mohit-trootech
    public | auth_group_id_seq                 | sequence | mohit-trootech
    public | auth_group_permissions            | table    | mohit-trootech
    public | auth_group_permissions_id_seq     | sequence | mohit-trootech
    public | auth_permission                   | table    | mohit-trootech
    public | auth_permission_id_seq            | sequence | mohit-trootech
    public | auth_user                         | table    | mohit-trootech
    public | auth_user_groups                  | table    | mohit-trootech
    public | auth_user_groups_id_seq           | sequence | mohit-trootech
    public | auth_user_id_seq                  | sequence | mohit-trootech
    public | auth_user_user_permissions        | table    | mohit-trootech
    public | auth_user_user_permissions_id_seq | sequence | mohit-trootech
    public | django_admin_log                  | table    | mohit-trootech
    public | django_admin_log_id_seq           | sequence | mohit-trootech
    public | django_content_type               | table    | mohit-trootech
    public | django_content_type_id_seq        | sequence | mohit-trootech
    public | django_migrations                 | table    | mohit-trootech
    public | django_migrations_id_seq          | sequence | mohit-trootech
    public | django_session                    | table    | mohit-trootech
    (19 rows)

By default, INSTALLED_APPS contains the following apps, all of which come with Django:

- django.contrib.admin – The admin site. You’ll use it shortly.
- django.contrib.auth – An authentication system.
- django.contrib.contenttypes – A framework for content types.
- django.contrib.sessions – A session framework.
- django.contrib.messages – A messaging framework.
- django.contrib.staticfiles – A framework for managing static files.

These applications are included by default as a convenience for the common case.

<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet" />

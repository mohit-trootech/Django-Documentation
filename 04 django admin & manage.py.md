# django-admin and manage.py

Django-admin is Django’s command-line utility for administrative tasks.

- manage.py is automatically created in each Django project. It does the same thing as django-admin but also sets the DJANGO_SETTINGS_MODULE environment variable so that it points to your project’s settings.py file.

- The django-admin script should be on your system path if you installed Django via pip. If it’s not in your path, ensure you have your virtual environment activated.

Generally, when working on a single Django project, it’s easier to use manage.py than django-admin. If you need to switch between multiple Django settings files, use django-admin with DJANGO_SETTINGS_MODULE or the --settings command line option.

#### Usage

    django-admin <command> [options]
    manage.py <command> [options]
    python -m django <command> [options]

`command` should be one of the commands listed in this document. `options`, which is optional, should be zero or more of the options available for the given command.

---

# Available Commands

Run `django-admin help` to display usage information and a list of the commands provided by each application.

Run `django-admin help --commands` to display a list of all available commands.

Run `django-admin help <command>` to display a description of the given command and a list of its available options.

## App names

Many commands take a list of “`app names`.” An “app name” is the basename of the package containing your models. For example, if your INSTALLED_APPS contains the string 'mysite.blog', the app name is blog.

## 1. Check

    django-admin check [app_label [app_label ...]]

Uses the system check framework to inspect the entire Django project for common problems.

By default, all apps will be checked. You can check a subset of apps by providing a list of app labels as arguments:

    django-admin check auth admin myapp

<table class="table table-dark">
  <thead>
    <tr>
      <th scope="col">Command</th>
      <th scope="col">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row" rowspan="2"><code>--tag TAGS, -t TAGS</code> </th>
      <td>system check framework performs many different types of checks that are categorized with tags.</td>
    </tr>
    <tr>
      <td><code>django-admin check --tag models --tag compatibility</code></td>
    </tr>
    <tr>
      <th scope="row" rowspan="2"> <code>--database DATABASE</code> </th>
      <td>Specifies the database to run checks requiring database access</td>
    </tr>
    <tr>
      <td><code>django-admin check --database default --database other</code> </td>
    </tr>
     <tr>
      <th scope="row"> <code>--list-tags</code> </th>
      <td>Lists all available tags.</td>
    </tr>
    <tr>
    <th scope="row"><code>--fail-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}</code</th>
      <td><code>django-admin check --database default --database other</code> </td>
    </tr>
<tr>
    <th scope="row"><code>--deploy</code</th>
      <td>Specifies the message level that will cause the command to exit with a non-zero status. Default is ERROR.</td>
    </tr>
  </tbody>
</table>

You can use this option in your local development environment, but since your local development settings module may not have many of your production settings, you will probably want to point the check command at a different settings module, either by setting the `DJANGO_SETTINGS_MODULE` environment variable, or by passing the `--settings` option:

    django-admin check --deploy --settings=production_settings

Or you could run it directly on a production or staging deployment to verify that the correct settings are in use (omitting --settings). You could even make it part of your integration test suite.

## 2. compilemessages

    django-admin compilemessages

Compiles .po files created by makemessages to .mo files for use with the built-in gettext support.

<table class="table table-dark">
  <thead>
    <tr>
      <th scope="col">Command</th>
      <th scope="col">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row"><code>--locale LOCALE, -l LOCALE</code> </th>
      <td>Specifies the locale(s) to process. If not provided, all locales are processed.</td>
    </tr>
    <tr>
      <th scope="row"> <code>--exclude EXCLUDE, -x EXCLUDE</code> </th>
      <td>Specifies the locale(s) to exclude from processing. If not provided, no locales are excluded.</td>
    </tr>
     <tr>
      <th scope="row"> <code>--use-fuzzy, -f</code> </th>
      <td>Includes fuzzy translations into compiled files.</td>
    </tr>
    <tr>
    <th scope="row"><code>--fail-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}</code</th>
      <td><code>django-admin check --database default --database other</code> </td>
    </tr>
<tr>
    <th scope="row"><code>--ignore PATTERN, -i PATTERN</code</th>
      <td>Ignores directories matching the given glob-style pattern. Use multiple times to ignore more.</td>
    </tr>
  </tbody>
</table>

Example usage:

    django-admin compilemessages --locale=pt_BR
    django-admin compilemessages --locale=pt_BR --locale=fr -f
    django-admin compilemessages -l pt_BR
    django-admin compilemessages -l pt_BR -l fr --use-fuzzy
    django-admin compilemessages --exclude=pt_BR
    django-admin compilemessages --exclude=pt_BR --exclude=fr
    django-admin compilemessages -x pt_BR
    django-admin compilemessages -x pt_BR -x fr

Example usage:

    django-admin compilemessages --ignore=cache --ignore=outdated/*/locale

## 3. createcachetable

`django-admin createcachetable`

Creates the cache tables for use with the database cache backend using the information from your settings file. See Django’s cache framework for more information.

<table class="table table-dark">
  <thead>
    <tr>
      <th scope="col">Command</th>
      <th scope="col">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row"><code>--database DATABASE</code> </th>
      <td>Specifies the database in which the cache table(s) will be created. Defaults to default.</td>
    </tr>
    <tr>
      <th scope="row"> <code>--dry-run</code> </th>
      <td>Prints the SQL that would be run without actually running it, so you can customize it or use the migrations framework.</td>
    </tr>
  </tbody>
</table>

## 4. dbshell

`django-admin dbshell`

Runs the command-line client for the database engine specified in your ENGINE setting, with the connection parameters specified in your USER, PASSWORD, etc., settings.

- For PostgreSQL, this runs the psql command-line client.
- For MySQL, this runs the mysql command-line client.
- For SQLite, this runs the sqlite3 command-line client.
- For Oracle, this runs the sqlplus command-line client.

This command assumes the programs are on your PATH so that a call to the program name (psql, mysql, sqlite3, sqlplus) will find the program in the right place. There’s no way to specify the location of the program manually.

<table class="table table-dark">
  <thead>
    <tr>
      <th scope="col">Command</th>
      <th scope="col">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row"><code>--database DATABASE</code> </th>
      <td>Specifies the database onto which to open a shell. Defaults to default.</td>
    </tr>
    <tr>
      <th scope="row"> <code>-- ARGUMENTS</code> </th>
      <td>Any arguments following a `--` divider will be passed on to the underlying command-line client.</td>
    </tr>
  </tbody>
</table>

For example, with PostgreSQL you can use the `psql` command’s flag to execute a raw SQL query directly:

![image-2.png](attachment:image-2.png)

    django-admin dbshell -- -e "select user()"

*if user available in database*

## 5. dumpdata

    django-admin dumpdata [app_label[.ModelName] [app_label[.ModelName] ...]]

Outputs to standard output all data in the database associated with the named application(s).

If no application name is provided, all installed applications will be dumped.

The output of dumpdata can be used as input for loaddata.

When result of dumpdata is saved as a file, it can serve as a fixture for tests or as an initial data.

<table class="table table-dark">
  <thead>
    <tr>
      <th scope="col">Command</th>
      <th scope="col">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row"><code>--all, -a</code> </th>
      <td>Uses Django’s base manager, dumping records which might otherwise be filtered or modified by a custom manager</td>
    </tr>
    <tr>
      <th scope="row"> <code>--format FORMAT</code> </th>
      <td>Specifies the serialization format of the output. Defaults to JSON. Supported formats are listed in Serialization formats.</td>
    </tr>
     <tr>
      <th scope="row"> <code>--indent INDENT</code> </th>
      <td>Specifies the number of indentation spaces to use in the output. Defaults to None which displays all data on single line.</td>
    </tr>
    <tr>
    <th scope="row"><code>--exclude EXCLUDE, -e EXCLUDE</code</th>
      <td><code>Prevents specific applications or models (specified in the form of app_label.ModelName) from being dumped. If you specify a model name, then only that model will be excluded</code> </td>
    </tr>
    <tr>
    <th scope="row"><code>--database DATABASE</code</th>
      <td>Specifies the database from which data will be dumped. Defaults to default.</td>
    </tr>
    <tr>
    <th scope="row"><code>--natural-foreign</code</th>
      <td>Uses the natural_key() model method to serialize any foreign key and many-to-many relationship to objects of the type that defines the method.</td>
    </tr>
    <tr>
    <th scope="row"><code>--natural-primary</code</th>
      <td>Omits the primary key in the serialized data of this object since it can be calculated during deserialization.</td>
    </tr>
    <tr>
    <th scope="row"><code>--output OUTPUT, -o OUTPUT</code</th>
      <td>Specifies a file to write the serialized data to. By default, the data goes to standard output.</td>
    </tr>
  </tbody>
</table>

When this option is set and --verbosity is greater than 0 (the default), a progress bar is shown in the terminal.

    django-admin dumpdata -o mydata.json.gz

![image-3.png](attachment:image-3.png)

## 6. flush

    django-admin flush

Removes all data from the database and re-executes any post-synchronization handlers. The table of which migrations have been applied is not cleared.

If you would rather start from an empty database and rerun all migrations, you should drop and recreate the database and then run migrate instead.

`--noinput, --no-input`

Suppresses all user prompts.

`--database DATABASE`

Specifies the database to flush. Defaults to default.

## 7. inspectdb

    django-admin inspectdb [table [table ...]]

Introspects the database tables in the database pointed-to by the NAME setting and outputs a Django model module (a models.py file) to standard output.

## 8. loaddata

  django-admin loaddata fixture [fixture ...]

Searches for and loads the contents of the named fixture into the database.

<table class="table table-dark">
  <thead>
    <tr>
      <th scope="col">Command</th>
      <th scope="col">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row"><code>--database DATABASE</code> </th>
      <td>Specifies the database into which the data will be loaded. Defaults to default.</td>
    </tr>
    <tr>
      <th scope="row"> <code>--ignorenonexistent, -i</code> </th>
      <td>Ignores fields and models that may have been removed since the fixture was originally generated.</td>
    </tr>
     <tr>
      <th scope="row"> <code>--app APP_LABEL</code> </th>
      <td>Specifies a single app to look for fixtures in rather than looking in all apps.</td>
    </tr>
    <tr>
    <th scope="row"><code>--exclude EXCLUDE, -e EXCLUDE</code</th>
      <td><code>Excludes loading the fixtures from the given applications and/or models (in the form of app_label or app_label.ModelName).</code> </td>
    </tr>
    <tr>
    <th scope="row"><code>--database DATABASE</code</th>
      <td>Specifies the database from which data will be dumped. Defaults to default.</td>
    </tr>
    <tr>
    <th scope="row"><code>--natural-foreign</code</th>
      <td>Uses the natural_key() model method to serialize any foreign key and many-to-many relationship to objects of the type that defines the method.</td>
    </tr>
    <tr>
    <th scope="row"><code>--natural-primary</code</th>
      <td>Omits the primary key in the serialized data of this object since it can be calculated during deserialization.</td>
    </tr>
    <tr>
    <th scope="row"><code>--output OUTPUT, -o OUTPUT</code</th>
      <td>Specifies a file to write the serialized data to. By default, the data goes to standard output.</td>
    </tr>
  </tbody>
</table>

*Use the option multiple times to exclude more than one app or model.*

***Loading fixtures from stdin***

You can use a dash `--` as the fixture name to load input from sys.stdin. For example:

  django-admin loaddata --format=json -

Loading from stdin is useful with standard input and output redirections. For example:

    django-admin dumpdata --format=json --database=test app_label.ModelName

    django-admin loaddata --format=json --database=prod -

The dumpdata command can be used to generate input for loaddata.

## 9. makemessages

    django-admin makemessages

Runs over the entire source tree of the current directory and pulls out all strings marked for translation. It creates (or updates) a message file in the conf/locale (in the Django tree) or locale (for project and application) directory. After making changes to the messages files you need to compile them with compilemessages for use with the builtin gettext support.

<table class="table table-dark">
  <thead>
    <tr>
      <th scope="col">Command</th>
      <th scope="col">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row"><code>--all, -a</code> </th>
      <td>Updates the message files for all available languages.</td>
    </tr>
    <tr>
      <th scope="row"> <code>--extension EXTENSIONS, -e EXTENSIONS</code> </th>
      <td>Specifies a list of file extensions to examine (default: html, txt, py or js if --domain is djangojs).</td>
    </tr>
     <tr>
      <th scope="row"> <code>--locale LOCALE, -l LOCALE</code> </th>
      <td>Specifies the locale(s) to process.</td>
    </tr>
    <tr>
    <th scope="row"><code>--exclude EXCLUDE, -x EXCLUDE</code</th>
      <td><code>Specifies the locale(s) to exclude from processing. If not provided, no locales are excluded.</code> </td>
    </tr>
    <tr>
    <th scope="row"><code>--domain DOMAIN, -d DOMAIN</code</th>
      <td>Specifies the domain of the messages files.</td>
    </tr>
    <tr>
    <th scope="row"><code>--natural-foreign</code</th>
      <td>Uses the natural_key() model method to serialize any foreign key and many-to-many relationship to objects of the type that defines the method.</td>
    </tr>
    <tr>
    <th scope="row"><code>--natural-primary</code</th>
      <td>Omits the primary key in the serialized data of this object since it can be calculated during deserialization.</td>
    </tr>
    <tr>
    <th scope="row"><code>--output OUTPUT, -o OUTPUT</code</th>
      <td>Specifies a file to write the serialized data to. By default, the data goes to standard output.</td>
    </tr>
  </tbody>
</table>

Example usage:

    django-admin makemessages --locale=de --extension xhtml
Separate multiple extensions with commas or use -e or --extension multiple times:

Example usage:

    django-admin makemessages --locale=pt_BR
    django-admin makemessages --locale=pt_BR --locale=fr
    django-admin makemessages -l pt_BR
    django-admin makemessages -l pt_BR -l fr
    django-admin makemessages --exclude=pt_BR
    django-admin makemessages --exclude=pt_BR --exclude=fr
    django-admin makemessages -x pt_BR
    django-admin makemessages -x pt_BR -x fr

## 10. makemigrations

    django-admin makemigrations [app_label [app_label ...]]

Creates new migrations based on the changes detected to your models. Migrations, their relationship with apps and more are covered in depth in the migrations documentation.

<table class="table table-dark">
  <thead>
    <tr>
      <th scope="col">Command</th>
      <th scope="col">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row"><code>--noinput, --no-input</code> </th>
      <td>Suppresses all user prompts. If a suppressed prompt cannot be resolved automatically, the command will exit with error code 3.</td>
    </tr>
    <tr>
      <th scope="row"> <code>--empty</code> </th>
      <td>Outputs an empty migration for the specified apps, for manual editing. This is for advanced users and should not be used unless you are familiar with the migration format, migration operations, and the dependencies between your migrations.</td>
    </tr>
     <tr>
      <th scope="row"> <code>--dry-run</code> </th>
      <td>Shows what migrations would be made without actually writing any migrations files to disk.</td>
    </tr>
    <tr>
    <th scope="row"><code>--merge</code</th>
      <td><code>Enables fixing of migration conflicts.</code> </td>
    </tr>
    <tr>
    <th scope="row"><code>--name NAME, -n NAME</code</th>
      <td>Allows naming the generated migration(s) instead of using a generated name. The name must be a valid Python identifier.</td>
    </tr>
    <tr>
    <th scope="row"><code>--no-header</code</th>
      <td>Generate migration files without Django version and timestamp header.</td>
    </tr>
    <tr>
    <th scope="row"><code>--check</code</th>
      <td>Makes makemigrations exit with a non-zero status when model changes without migrations are detected. Implies --dry-run.</td>
    </tr>
    <tr>
    <th scope="row"><code>--output OUTPUT, -o OUTPUT</code</th>
      <td>Specifies a file to write the serialized data to. By default, the data goes to standard output.</td>
    </tr>
  </tbody>
</table>

*To add migrations to an app that doesn’t have a migrations directory, run makemigrations with the app’s app_label.*

## 11. migrate

    django-admin migrate [app_label] [migration_name]¶

Synchronizes the database state with the current set of models and migrations. Migrations, their relationship with apps and more are covered in depth in the migrations documentation.

*No arguments: All apps have all of their migrations run.*

`<app_label>`: The specified app has its migrations run, up to the most recent migration. This may involve running other apps’ migrations too, due to dependencies.

`<app_label> <migrationname>`: Brings the database schema to a state where the named migration is applied, but no later migrations in the same app are applied. This may involve unapplying migrations if you have previously migrated past the named migration. You can use a prefix of the migration name, e.g. 0001, as long as it’s unique for the given app name. Use the name zero to migrate all the way back i.e. to revert all applied migrations for an app.
Warning

*When unapplying migrations, all dependent migrations will also be unapplied, regardless of <app_label>. You can use --plan to check which migrations will be unapplied.*

<table class="table table-dark">
  <thead>
    <tr>
      <th scope="col">Command</th>
      <th scope="col">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row"><code>--database DATABASE</code> </th>
      <td>Specifies the database to migrate. Defaults to default.</td>
    </tr>
    <tr>
      <th scope="row"> <code>--fake</code> </th>
      <td>Marks the migrations as applied, but without actually running the SQL to change your database schema.</td>
    </tr>
     <tr>
      <th scope="row"> <code>--fake-initial</code> </th>
      <td>Allows Django to skip an app’s initial migration if all database tables with the names of all models created by all CreateModel operations in that migration already exist.</td>
    </tr>
    <tr>
    <th scope="row"><code>--plan</code</th>
      <td><code>Shows the migration operations that will be performed for the given migrate command.</code> </td>
    </tr>
    <tr>
    <th scope="row"><code>--run-syncdb</code</th>
      <td>Allows creating tables for apps without migrations. While this isn’t recommended</td>
    </tr>
    <tr>
    <th scope="row"><code>--noinput, --no-input</code</th>
      <td>Suppresses all user prompts. An example prompt is asking about removing stale content types.</td>
    </tr>
    <tr>
    <th scope="row"><code>--check</code</th>
      <td>Makes migrate exit with a non-zero status when unapplied migrations are detected.</td>
    </tr>
    <tr>
    <th scope="row"><code>--prune</code</th>
      <td>Deletes nonexistent migrations from the django_migrations table.</td>
    </tr>
  </tbody>
</table>

*fake Migrations*
*This is intended for advanced users to manipulate the current migration state directly if they’re manually applying changes; be warned that using --fake runs the risk of putting the migration state table into a state where manual recovery will be needed to make migrations run correctly.*

`--prune: This is useful when migration files replaced by a squashed migration have been removed.`

## 12. optimizemigration

    django-admin optimizemigration app_label migration_name

Optimizes the operations for the named migration and overrides the existing file. If the migration contains functions that must be manually copied, the command creates a new migration file suffixed with _optimized that is meant to replace the named migration.

`--check` Makes optimizemigration exit with a non-zero status when a migration can be optimized.

## 13. runserver

    django-admin runserver [addrport]

Starts a lightweight development web server on the local machine. By default, the server runs on port 8000 on the IP address 127.0.0.1. You can pass in an IP address and port number explicitly.

*The development server automatically reloads Python code for each request, as needed. You don’t need to restart the server for code changes to take effect. However, some actions like adding files don’t trigger a restart, so you’ll have to restart the server in these cases.*

***DO NOT USE THIS SERVER IN A PRODUCTION SETTING. It has not gone through security audits or performance tests. (And that’s how it’s gonna stay. We’re in the business of making web frameworks, not web servers, so improving this server to be able to handle a production environment is outside the scope of Django.)***

Note that the default IP address, 127.0.0.1, is not accessible from other machines on your network. To make your development server viewable to other machines on the network, use its own IP address (e.g. 192.168.2.1), 0 (shortcut for 0.0.0.0), 0.0.0.0, or :: (with IPv6 enabled).

*NOTE: If you’re using Linux or MacOS and install both pywatchman and the Watchman service, kernel signals will be used to autoreload the server (rather than polling file modification timestamps each second). This offers better performance on large projects, reduced response time after code changes, more robust change detection, and a reduction in power usage. Django supports pywatchman 1.2.0 and higher.*

*NOTE: When you start the server, and each time you change Python code while the server is running, the system check framework will check your entire Django project for some common errors (see the check command). If any errors are found, they will be printed to standard output. You can use the -`-skip-checks` option to skip running system checks.*

You can run as many concurrent servers as you want, as long as they’re on separate ports by executing django-admin runserver more than once.

You can provide an IPv6 address surrounded by brackets (e.g. [200a::1]:8000). This will automatically enable IPv6 support.

A hostname containing ASCII-only characters can also be used.

If the staticfiles contrib app is enabled (default in new projects) the runserver command will be overridden with its own runserver command.

Logging of each request and response of the server is sent to the django.server logger.

<table class="table table-dark">
  <thead>
    <tr>
      <th scope="col">Command</th>
      <th scope="col">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row"><code>--noreload</code> </th>
      <td>Disables the auto-reloader.</td>
    </tr>
    <tr>
      <th scope="row"> <code>--nothreading</code> </th>
      <td>Disables use of threading in the development server. The server is multithreaded by default.</td>
    </tr>
     <tr>
      <th scope="row"> <code>--ipv6, -6</code> </th>
      <td>Uses IPv6 for the development server. This changes the default IP address from 127.0.0.1 to ::1.</td>
    </tr>
    <tr>
    <th scope="row"><code>--plan</code</th>
      <td><code>Shows the migration operations that will be performed for the given migrate command.</code> </td>
    </tr>
    <tr>
    <th scope="row"><code>--run-syncdb</code</th>
      <td>Allows creating tables for apps without migrations. While this isn’t recommended</td>
    </tr>
    <tr>
    <th scope="row"><code>--noinput, --no-input</code</th>
      <td>Suppresses all user prompts. An example prompt is asking about removing stale content types.</td>
    </tr>
    <tr>
    <th scope="row"><code>--check</code</th>
      <td>Makes migrate exit with a non-zero status when unapplied migrations are detected.</td>
    </tr>
    <tr>
    <th scope="row"><code>--prune</code</th>
      <td>Deletes nonexistent migrations from the django_migrations table.</td>
    </tr>
  </tbody>
</table>

Examples of using different ports and addresses

Port 8000 on IP address 127.0.0.1:

    django-admin runserver

Port 8000 on IP address 1.2.3.4:

    django-admin runserver 1.2.3.4:8000

Port 7000 on IP address 127.0.0.1:

    django-admin runserver 7000

Port 7000 on IP address 1.2.3.4:

    django-admin runserver 1.2.3.4:7000

Port 8000 on IPv6 address ::1:

    django-admin runserver -6

Port 7000 on IPv6 address ::1:

    django-admin runserver -6 7000

Port 7000 on IPv6 address 2001:0db8:1234:5678::9:

    django-admin runserver [2001:0db8:1234:5678::9]:7000

Port 8000 on IPv4 address of host localhost:

    django-admin runserver localhost:8000

Port 8000 on IPv6 address of host localhost:

    django-admin runserver -6 localhost:8000

## 14. sendtestemail

    django-admin sendtestemail [email [email ...]]

Sends a test email (to confirm email sending through Django is working) to the recipient(s) specified.

For example:

    django-admin sendtestemail foo@example.com bar@example.com

There are a couple of options, and you may use any combination of them together:

`--managers`

Mails the email addresses specified in MANAGERS using mail_managers().

`--admins`
Mails the email addresses specified in ADMINS using mail_admins().

## 15. shell

    django-admin shell

Starts the Python interactive interpreter.

`--interface {ipython,bpython,python}, -i {ipython,bpython,python}`

Specifies the shell to use. By default, Django will use IPython or bpython if either is installed. If both are installed, specify which one you want like so:

IPython:

    django-admin shell -i ipython

bpython:

    django-admin shell -i bpython

If you have a “rich” shell installed but want to force use of the “plain” Python interpreter, use python as the interface name, like so:

    django-admin shell -i python

`--nostartup`

Disables reading the startup script for the “plain” Python interpreter. By default, the script pointed to by the PYTHONSTARTUP environment variable or the ~/.pythonrc.py script is read.

`--command COMMAND, -c COMMAND`

Lets you pass a command as a string to execute it as Django, like so:

    django-admin shell --command="import django; print(django.__version__)"

    $ django-admin shell <<EOF
    > import django
    > print(django.__version__)
    > EOF

## 16. showmigrations

    django-admin showmigrations [app_label [app_label ...]]

Shows all migrations in a project. You can choose from one of two formats:

<table class="table table-dark">
  <thead>
    <tr>
      <th scope="col">Command</th>
      <th scope="col">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row"><code>--list, -l</code> </th>
      <td>Lists all of the apps Django knows about, the migrations available for each app, and whether or not each migration is applied (marked by an [X] next to the migration name).</td>
    </tr>
    <tr>
      <th scope="row"> <code>--plan, -p</code> </th>
      <td>Shows the migration plan Django will follow to apply migrations. Like --list, applied migrations are marked by an [X].</td>
    </tr>
     <tr>
      <th scope="row"> <code>--database DATABASE</code> </th>
      <td>Specifies the database to examine. Defaults to default.</td>
    </tr>
    <tr>
    <th scope="row"><code>--plan</code</th>
      <td><code>Shows the migration operations that will be performed for the given migrate command.</code> </td>
    </tr>
    <tr>
  </tbody>
</table>

## 17. sqlflush

    django-admin sqlflush

Prints the SQL statements that would be executed for the flush command.

    --database DATABASE

Specifies the database for which to print the SQL. Defaults to default.

## 18. sqlmigrate

    django-admin sqlmigrate app_label migration_name

Prints the SQL for the named migration. This requires an active database connection, which it will use to resolve constraint names; this means you must generate the SQL against a copy of the database you wish to later apply it on.

`--backwards`

Generates the SQL for unapplying the migration. By default, the SQL created is for running the migration in the forwards direction.

`--database DATABASE`

Specifies the database for which to generate the SQL. Defaults to default.

## 19. sqlsequencereset

    django-admin sqlsequencereset app_label [app_label ...]

Prints the SQL statements for resetting sequences for the given app name(s).

Sequences are indexes used by some database engines to track the next available number for automatically incremented fields.

Use this command to generate SQL which will fix cases where a sequence is out of sync with its automatically incremented field data.

`--database DATABASE`

Specifies the database for which to print the SQL. Defaults to default.

## 20. squashmigrations

    django-admin squashmigrations app_label [start_migration_name] migration_name

Squashes the migrations for app_label up to and including migration_name down into fewer migrations, if possible. The resulting squashed migrations can live alongside the unsquashed ones safely.

When start_migration_name is given, Django will only include migrations starting from and including this migration. This helps to mitigate the squashing limitation of RunPython and django.db.migrations.operations.RunSQL migration operations.

<table class="table table-dark">
  <thead>
    <tr>
      <th scope="col">Command</th>
      <th scope="col">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row"><code>--no-optimize</code> </th>
      <td>Disables the optimizer when generating a squashed migration. By default, Django will try to optimize the operations in your migrations to reduce the size of the resulting file.</td>
    </tr>
    <tr>
      <th scope="row"> <code>--noinput, --no-input</code> </th>
      <td>Suppresses all user prompts.</td>
    </tr>
     <tr>
      <th scope="row"> <code>--squashed-name SQUASHED_NAME</code> </th>
      <td>Sets the name of the squashed migration. When omitted, the name is based on the first and last migration, with _squashed_ in between.</td>
    </tr>
    <tr>
    <th scope="row"><code>--no-header</code</th>
      <td><code>Generate squashed migration file without Django version and timestamp header.</code> </td>
    </tr>
    <tr>
  </tbody>
</table>

## 21. startapp

    django-admin startapp name [directory]

Creates a Django app directory structure for the given app name in the current directory or the given destination.

By default, the new directory contains a models.py file and other app template files. If only the app name is given, the app directory will be created in the current working directory.

If the optional destination is provided, Django will use that existing directory rather than creating a new one. You can use `‘.’` to denote the current working directory.

For example:

    django-admin startapp myapp /Users/jezdez/Code/myapp

`--template TEMPLATE`

Provides the path to a directory with a custom app template file, or a path to an uncompressed archive (.tar) or a compressed archive (.tar.gz, .tar.bz2, .tar.xz, .tar.lzma, .tgz, .tbz2, .txz, .tlz, .zip) containing the app template files.

For example,

    django-admin startapp --template=/Users/jezdez/Code/my_app_template myapp

Django will also accept URLs (http, https, ftp) to compressed archives with the app template files, downloading and extracting them on the fly.

For example,

    django-admin startapp --template=https://github.com/githubuser/django-app-template/archive/main.zip myapp

<table class="table table-dark">
  <thead>
    <tr>
      <th scope="col">Command</th>
      <th scope="col">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row"><code>--extension EXTENSIONS, -e EXTENSIONS</code> </th>
      <td>--extension EXTENSIONS, -e EXTENSIONS</td>
    </tr>
    <tr>
      <th scope="row"> <code>--name FILES, -n FILES</code> </th>
      <td>Specifies which files in the app template (in addition to those matching --extension) should be rendered with the template engine. Defaults to an empty list.</td>
    </tr>
     <tr>
      <th scope="row"> <code>--exclude DIRECTORIES, -x DIRECTORIES</code> </th>
      <td>Specifies which directories in the app template should be excluded, in addition to `.git` and `pycache.py` If this option is not provided, directories named pycache or starting with . will be excluded.</td>
    </tr>
  </tbody>
</table>

The template context used for all matching files is:

## 22. startproject

    django-admin startproject name [directory]

Creates a Django project directory structure for the given project name in the current directory or the given destination.

By default, the new directory contains manage.py and a project package (containing a settings.py and other files).

If only the project name is given, both the project directory and project package will be named `<projectname>` and the project directory will be created in the current working directory.

If the optional destination is provided, Django will use that existing directory as the project directory, and create manage.py and the project package within it. Use ‘.’ to denote the current working directory.

For example:

    django-admin startproject myproject /Users/jezdez/Code/myproject_repo

<table class="table table-dark">
  <thead>
    <tr>
      <th scope="col">Command</th>
      <th scope="col">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row"><code>--template TEMPLATE</code> </th>
      <td>Specifies a directory, file path, or URL of a custom project template.</td>
    </tr>
    <tr>
      <th scope="row"> <code>--extension EXTENSIONS, -e EXTENSIONS</code> </th>
      <td>Specifies which file extensions in the project template should be rendered with the template engine. Defaults to py.</td>
    </tr>
     <tr>
      <th scope="row"> <code>--name FILES, -n FILES</code> </th>
      <td>Specifies which files in the project template (in addition to those matching --extension) should be rendered with the template engine. Defaults to an empty list..</td>
    </tr>
    <tr>
    <th scope="row"><code>--exclude DIRECTORIES, -x DIRECTORIES</code</th>
      <td>Specifies which directories in the project template should be excluded, in addition to .git and __pycache__.</td>
    </tr>
  </tbody>
</table>

The template context used is:

Any option passed to the startproject command (among the command’s supported options)

    project_name – the project name as passed to the command
    project_directory – the full path of the newly created project
    secret_key – a random key for the SECRET_KEY setting
    docs_version – the version of the documentation: 'dev' or '1.x'
    django_version – the version of Django, e.g. '2.0.3'

## 23. test

    django-admin test [test_label [test_label ...]]

Runs tests for all installed apps.

## 24. testserver

    django-admin testserver [fixture [fixture ...]]

Runs a Django development server (as in runserver) using data from the given fixture(s).

---

# Django Contril Commands

## 1. changepassword

    django-admin changepassword [<username>]
    django-admin changepassword ringo

## 2. createsuperuser

    django-admin createsuperuser
    DJANGO_SUPERUSER_PASSWORD

---

# django.contrib.contenttypes

## 1. remove_stale_contenttypes

    django-admin remove_stale_contenttypes

This command is only available if Django’s contenttypes app (django.contrib.contenttypes) is installed.

---

# django.contrib.sessions

## 1. clearsessions

    django-admin clearsessions

Can be run as a cron job or directly to clean out expired sessions.

---

# django.contrib.staticfiles

## 1. collectstatic

This command is only available if the static files application (django.contrib.staticfiles) is installed.

## 2. findstatic

This command is only available if the static files application (django.contrib.staticfiles) is installed.

<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet" />

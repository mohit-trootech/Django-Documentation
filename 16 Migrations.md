<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet" />

# Migrations

Migrations are Django’s way of propagating changes you make to your models (adding a field, deleting a model, etc.) into your database schema. They’re designed to be mostly automatic, but you’ll need to know when to make migrations, when to run them, and the common problems you might run into.

## The Commands

There are several commands which you will use to interact with migrations and Django’s handling of database schema:

<table class="table table-hover">
    <thead>
        <tr>
            <th>Command</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <th>migrate</th>
            <td>responsible for applying and unapplying migrations.</td>
        </tr>
        <tr>
            <th>makemigrations</th>
            <td>responsible for creating new migrations based on the changes you have made to your models.</td>
        </tr>
        <tr>
            <th>showmigrations</th>
            <td>lists a project’s migrations and their status.</td>
        </tr>
        <tr>
            <th>sqlmigrate</th>
            <td>displays the SQL statements for a migration.</td>
        </tr>
    </tbody>
</table>

The migration files for each app live in a “migrations” directory inside of that app, and are designed to be committed to, and distributed as part of, its codebase. You should be making them once on your development machine and then running the same migrations on your colleagues’ machines, your staging machines, and eventually your production machines.

## Workflow

Django can create migrations for you. Make changes to your models - say, add a field and remove a model - and then run makemigrations:

    $ python manage.py makemigrations
    Migrations for 'books':
    books/migrations/0003_auto.py:
        - Alter field author on book

Your models will be scanned and compared to the versions currently contained in your migration files, and then a new set of migrations will be written out. Make sure to read the output to see what makemigrations thinks you have changed - it’s not perfect, and for complex changes it might not be detecting what you expect.

Once you have your new migration files, you should apply them to your database to make sure they work as expected:

    $ python manage.py migrate
    Operations to perform:
    Apply all migrations: books
    Running migrations:
    Rendering model states... DONE
    Applying books.0003_auto... OK

Once the migration is applied, commit the migration and the models change to your version control system as a single commit - that way, when other developers (or your production servers) check out the code, they’ll get both the changes to your models and the accompanying migration at the same time.

If you want to give the migration(s) a meaningful name instead of a generated one, you can use the `makemigrations --name` option:

    python manage.py makemigrations --name changed_my_model your_app_label

## Version control

Because migrations are stored in version control, you’ll occasionally come across situations where you and another developer have both committed a migration to the same app at the same time, resulting in two migrations with the same number.

Don’t worry - the numbers are just there for developers’ reference, Django just cares that each migration has a different name. Migrations specify which other migrations they depend on - including earlier migrations in the same app - in the file, so it’s possible to detect when there’s two new migrations for the same app that aren’t ordered.

When this happens, Django will prompt you and give you some options. If it thinks it’s safe enough, it will offer to automatically linearize the two migrations for you. If not, you’ll have to go in and modify the migrations yourself.

## Transactions

On databases that support DDL transactions (SQLite and PostgreSQL), all migration operations will run inside a single transaction by default. In contrast, if a database doesn’t support DDL transactions (e.g. MySQL, Oracle) then all operations will run without a transaction.

You can prevent a migration from running in a transaction by setting the atomic attribute to False. For example:

    from django.db import migrations

    class Migration(migrations.Migration):
        atomic = False

It’s also possible to execute parts of the migration inside a transaction using atomic() or by passing atomic=True to RunPython. See Non-atomic migrations for more details.

## Dependencies

While migrations are per-app, the tables and relationships implied by your models are too complex to be created for one app at a time. When you make a migration that requires something else to run - for example, you add a ForeignKey in your books app to your authors app - the resulting migration will contain a dependency on a migration in author

*We will Learn About Dependencies in Next Module*

## Migration files

Migrations are stored as an on-disk format, referred to here as “migration files”. These files are actually normal Python files with an agreed-upon object layout, written in a declarative style.

A basic migration file looks like this:

    from django.db import migrations, models

    class Migration(migrations.Migration):
        dependencies = [("migrations", "0001_initial")]

        operations = [
            migrations.DeleteModel("Tribble"),
            migrations.AddField("Author", "rating", models.IntegerField(default=0)),
        ]

## Model managers

You can optionally serialize managers into migrations and have them available in RunPython operations. This is done by defining a use_in_migrations attribute on the manager class:

    class MyManager(models.Manager):
        use_in_migrations = True

    class MyModel(models.Model):
        objects = MyManager()

If you are using the from_queryset() function to dynamically generate a manager class, you need to inherit from the generated class to make it importable:

    class MyManager(MyBaseManager.from_queryset(CustomQuerySet)):
        use_in_migrations = True

    class MyModel(models.Model):
        objects = MyManager()

## Adding Migrations to Specific App

New apps come preconfigured to accept migrations, and so you can add migrations by running makemigrations once you’ve made some changes.

    python manage.py makemigrations your_app_label

## Revert Migrations

Migrations can be reversed with migrate by passing the number of the previous migration. For example, to reverse migration books.0003:

    $ python manage.py migrate books 0002
    Operations to perform:
    Target specific migration: 0002_auto, from books
    Running migrations:
    Rendering model states... DONE
    Unapplying books.0003_auto... OK

If you want to reverse all migrations applied for an app, use the name zero:

    $ python manage.py migrate books zero
    Operations to perform:
    Unapply all migrations: books
    Running migrations:
    Rendering model states... DONE
    Unapplying books.0002_auto... OK
    Unapplying books.0001_initial... OK
A migration is irreversible if it contains any irreversible operations. Attempting to reverse such migrations will raise IrreversibleError:

    $ python manage.py migrate books 0002
    Operations to perform:
    Target specific migration: 0002_auto, from books
    Running migrations:
    Rendering model states... DONE
    Unapplying books.0003_auto...Traceback (most recent call last):
    django.db.migrations.exceptions.IrreversibleError: Operation <RunSQL  sql='DROP TABLE demo_books'> in books.0003_auto is not reversible

## Squashing migrations

Now, This is something when you came a long way in your project and when you see migrations they are 100s of migrations file with some minor changes. How can we merge all these migrations into one, Here comes the concept of squashing.

Squashing is the act of reducing an existing set of many migrations down to one (or sometimes a few) migrations which still represent the same changes.

Django does this by taking all of your existing migrations, extracting their Operations and putting them all in sequence, and then running an optimizer over them to try and reduce the length of the list - for example, it knows that CreateModel and DeleteModel cancel each other out, and it knows that AddField can be rolled into CreateModel.

Once the operation sequence has been reduced as much as possible - the amount possible depends on how closely intertwined your models are and if you have any RunSQL or RunPython operations (which can’t be optimized through unless they are marked as elidable) - Django will then write it back out into a new set of migration files.

These files are marked to say they replace the previously-squashed migrations, so they can coexist with the old migration files, and Django will intelligently switch between them depending where you are in the history. If you’re still part-way through the set of migrations that you squashed, it will keep using them until it hits the end and then switch to the squashed history, while new installs will use the new squashed migration and skip all the old ones.

This enables you to squash and not mess up systems currently in production that aren’t fully up-to-date yet. The recommended process is to squash, keeping the old files, commit and release, wait until all systems are upgraded with the new release (or if you’re a third-party project, ensure your users upgrade releases in order without skipping any), and then remove the old files, commit and do a second release.

    $ ./manage.py squashmigrations myapp 0004
    Will squash the following migrations:

    - 0001_initial
    - 0002_some_change
    - 0003_another_change
    - 0004_undo_something
    Do you wish to proceed? [yN] y
    Optimizing...
    Optimized from 12 operations to 7 operations.
    Created new squashed migration /home/andrew/Programs/DjangoTest/test/migrations/0001_squashed_0004_undo_something.py
    You should commit this migration but leave the old ones in place;
    the new migration will be used for new installs. Once you are sure
    all instances of the codebase have applied the migrations you squashed,
    you can delete them.
Use the `squashmigrations --squashed-name` option if you want to set the name of the squashed migration rather than use an autogenerated one.

Note that model interdependencies in Django can get very complex, and squashing may result in migrations that do not run; either mis-optimized (in which case you can try again with --no-optimize, though you should also report an issue), or with a CircularDependencyError, in which case you can manually resolve it.

Once you’ve squashed your migration, you should then commit it alongside the migrations it replaces and distribute this change to all running instances of your application, making sure that they run migrate to store the change in their database.

You must then transition the squashed migration to a normal migration by:

Deleting all the migration files it replaces.
Updating all migrations that depend on the deleted migrations to depend on the squashed migration instead.
Removing the replaces attribute in the Migration class of the squashed migration (this is how Django tells that it is a squashed migration).

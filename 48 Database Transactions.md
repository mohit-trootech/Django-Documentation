<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet"/>

# Database transactions

Django gives you a few ways to control how database transactions are managed.

## Django’s default transaction behavior

Django’s default behavior is to run in autocommit mode. Each query is immediately committed to the database, unless a transaction is active
Django uses transactions or savepoints automatically tov guarantee the integrity of ORM operations that require multiple queries, especially *`delete()`* and *`update()`* queries.

## Tying transactions to HTTP requests

A common way to handle transactions on the web is to wrap each request in a transaction. Set ATOMIC_REQUESTS to True in the configuration of each database for which you want to enable this behavior.

It works like this. Before calling a view function, Django starts a transaction. If the response is produced without problems, Django commits the transaction. If the view produces an exception, Django rolls back the transaction.

```python
DATABASES = {
    "default": {
        ...,
        "ATOMIC_REQUESTS": True,
    }
}
```

***While the simplicity of this transaction model is appealing, it also makes it inefficient when traffic increases. Opening a transaction for every view has some overhead. The impact on performance depends on the query patterns of your application and on how well your database handles locking.***

this feature wraps every view function in the *`atomic()`* decorator

```python
from django.db import transaction


@transaction.non_atomic_requests
def my_view(request):
    do_stuff()


@transaction.non_atomic_requests(using="other")
def my_other_view(request):
    do_stuff_on_the_other_database()
```

## Controlling Transactions Explicitly

Django provides a single API to control database transactions.

```python
atomic[using=None, savepoint=True, durable=False]
```

Can be used as Decorator,

```python
from django.db import transaction


@transaction.atomic
def viewfunc(request):
    # This code executes inside a transaction.
    do_stuff()
```

OR, as a Context Manager

```python
from django.db import transaction


def viewfunc(request):
    # This code executes in autocommit mode (Django's default).
    do_stuff()

    with transaction.atomic():
        # This code executes inside a transaction.
        do_more_stuff()
```

## Handling IntegrityError

Wrapping atomic in a try/except block allows for natural handling of integrity errors:

```python
from django.db import IntegrityError, transaction

@transaction.atomic
def viewfunc(request):
    create_parent()

    try:
        with transaction.atomic():
            generate_relationships()
    except IntegrityError:
        handle_exception()

    add_children()
```

When exiting an atomic block, Django looks at whether it’s exited normally or with an exception to determine whether to commit or roll back. If you catch and handle exceptions inside an atomic block, you may hide from Django the fact that a problem has happened. This can result in unexpected behavior.

This is mostly a concern for DatabaseError and its subclasses such as IntegrityError. After such an error, the transaction is broken and Django will perform a rollback at the end of the atomic block. If you attempt to run database queries before the rollback happens, Django will raise a TransactionManagementError. You may also encounter this behavior when an ORM-related signal handler raises an exception.

```python
from django.db import DatabaseError, transaction

obj = MyModel(active=False)
obj.active = True
try:
    with transaction.atomic():
        obj.save()
except DatabaseError:
    obj.active = False

if obj.active:
    ...
```

<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet"/>

# Auto Commits

In the SQL standards, each SQL query starts a transaction, unless one is already active. Such transactions must then be explicitly committed or rolled back.

This isn’t always convenient for application developers. To alleviate this problem, most databases provide an autocommit mode. When autocommit is turned on and no transaction is active, each SQL query gets wrapped in its own transaction. In other words, not only does each such query start a transaction, but the transaction also gets automatically committed or rolled back, depending on whether the query succeeded.

> Deactivate Transactions & AUTOCOMMIT

```python
DATABASES = {
    "default": {
        ...,
        "ATOMIC_REQUESTS": True,
        "AUTOCOMMIT":False
    }
}
```

## Performing Actions after commit

Sometimes you need to perform an action related to the current database transaction, but only if the transaction successfully commits. Examples might include a background task, an email notification, or a cache invalidation.

### on_commit()

allows you to register callbacks that will be executed after the open transaction is successfully committed:

```python
on_commit[func, using=None, robust=False]
```

Pass a function, or any callable, to on_commit():

```python
from django.db import transaction


def send_welcome_email(): ...


transaction.on_commit(send_welcome_email)
```

Callbacks will not be passed any arguments, but you can bind them with *`functools.partial()`*:

```python
from functools import partial

for user in users:
    transaction.on_commit(partial(send_invite_email, user=user))
```

*If you call on_commit() while there isn’t an open transaction, the callback will be executed immediately.*

### Order of execution

On-commit functions for a given transaction are executed in the order they were registered.

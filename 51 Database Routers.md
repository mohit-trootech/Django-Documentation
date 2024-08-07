<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet"/>

# Database routers

A database Router is a class that provides up to four methods:

1. db_for_read() - Suggest the database that should be used for read operations for objects of type model.
2. db_for_write() - Suggest the database that should be used for writes of objects of type Model.
3. allow_relation() - Return True if a relation between obj1 and obj2 should be allowed, False if the relation should be prevented, or None if the router has no opinion.
4. allow_migrate() - Determine if the migration operation is allowed to run on the database with alias db. Return True if the operation should run, False if it shouldn’t run, or None if the router has no opinion.

```python
class AppRouter:
    default_db = "default"
    sqlite_db = "sqlite"
    related_models = [Pizza, Topping]

    def db_for_read(self, model, **hints):
        if model in self.related_models:
            return self.sqlite_db
        return None

    def db_for_write(self, model, **hints):
        if model in self.related_models:
            return self.sqlite_db
        return None
```

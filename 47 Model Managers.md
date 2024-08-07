<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet" />

# Managers

A Manager is the interface through which database query operations are provided to Django models. At least one Manager exists for every model in a Django application.

## Manager Names

Django adds a Manager with the name objects to every Django model class. However, if you want to use objects as a field name, or if you want to use a name other than objects for the Manager, you can rename it on a per-model basis. To rename the Manager for a given class, define a class attribute of type models.Manager() on that model. For example:

```python
from django.db import models

class Person(models.Model):
    # ...
    people = models.Manager()
```

Using this example model, Person.objects will generate an AttributeError exception, but Person.people.all() will provide a list of all Person objects.

## Custom managers

You can use a custom Manager in a particular model by extending the base Manager class and instantiating your custom Manager in your model.

There are two reasons you might want to customize a Manager: to add extra Manager methods, and/or to modify the initial QuerySet the Manager returns.

```python
# Model
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
```

…the statement *`Book.objects.all()`* will return all books in the database.

You can override a Manager’s base QuerySet by overriding the Manager.*`get_queryset()`* method. *`get_queryset()`* should return a QuerySet with the properties you require.

```python
# First, define the Manager subclass.
class DahlBookManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(author="Roald Dahl")


# Then hook it into the Book model explicitly.
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)

    objects = models.Manager()  # The default manager.
    dahl_objects = DahlBookManager()  # The Dahl-specific manager.
```

With this sample model, Book.objects.all() will return all books in the database, but Book.dahl_objects.all() will only return the ones written by Roald Dahl.

```python
Book.dahl_objects.all()
Book.dahl_objects.filter(title="Matilda")
Book.dahl_objects.count()
```

## People, Author, Editor Example

```python
class AuthorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role="A")

class EditorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role="E")

class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=1, choices={"A":_("Author"), "E": _("Editor")})
    people = models.Manager()
    authors = AuthorManager()
    editors = EditorManager()
```

This example allows you to request Person.authors.all(), Person.editors.all(), and Person.people.all(), yielding predictable results.

## Custom Queryset

```python
class PersonQuerySet(models.QuerySet):
    def authors(self):
        return self.filter(role="A")

    def editors(self):
        return self.filter(role="E")

class PersonManager(models.Manager):
    def get_queryset(self):
        return PersonQuerySet(self.model, using=self._db)

    def authors(self):
        return self.get_queryset().authors()

    def editors(self):
        return self.get_queryset().editors()

class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=1, choices={"A":_("Author"), "E": _("Editor")})
    people = PersonManager()
```

## Creating a manager with QuerySet methods

In lieu of the above approach which requires duplicating methods on both the QuerySet and the Manager, QuerySet.as_manager() can be used to create an instance of Manager with a copy of a custom QuerySet’s methods:

```python
class Person(models.Model):
    ...
    people = PersonQuerySet.as_manager()
```

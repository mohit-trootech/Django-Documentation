<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet" />

# Performing Raw SQL Queries in Django

Django Provides Two method to perform raw sql queries,

1. `Manager.raw()` - Perform Queries and return Model instances.
2. `Custom SQL` - Skips the model later to perform raw sql.

## Manager.Raw()

The raw() manager method can be used to perform raw SQL queries that return model instances:

```sql
Manager.raw(raw_query, params=(), translations=None)
```

Suppose we have following model Class,

```python
class Person(models.Model):
    first_name = models.CharField(...)
    last_name = models.CharField(...)
    birth_date = models.DateField(...)
```

Then we can perform raw sql like this,

```python
>>> for p in Person.objects.raw("SELECT * FROM myapp_person"):
...     print(p)
...
John Smith
Jane Jones
```

<i>Note :- Where did the name of the Person table come from in that example?
By default, Django figures out a database table name by joining the model’s “app label” – the name you used in manage.py startapp – to the model’s class name, with an underscore between them. In the example we’ve assumed that the Person model lives in an app named myapp, so its table would be myapp_person.*</i>

<i>MySQL Coersion Error - When working with mysql remember to correct correct tycasting before running any sql query, Suppose we have a column with values "john", "Doe", and we are running query like this `Select * FROM table WHERE my_col = 0;` Now This Will return both the values due to mysql coersion error</i>

### 1. Mapping Queryset

The index of columns or fields doesn't matter during raw sql queries.

```python
>>> Person.objects.raw("SELECT id, first_name, last_name, birth_date FROM myapp_person")
>>> Person.objects.raw("SELECT last_name, birth_date, first_name, id FROM myapp_person")
```

Both Queries Above return Same Output

### 2. Namemapping

Matching is done by name. This means that you can use SQL’s AS clauses to map fields in the query to model fields. So if you had some other table that had Person data in it, you could easily map it into Person instances:

```python
>>> Person.objects.raw(
...     """
...     SELECT first AS first_name,
...            last AS last_name,
...            bd AS birth_date,
...            pk AS id,
...     FROM some_other_table
...     """
... )
```

### 3. Translations

Alternatively, you can map fields in the query to model fields using the *translations* argument to raw(). This is a dictionary mapping names of fields in the query to names of fields on the model. For example, the above query could also be written:

```python
>>> name_map = {"first": "first_name", "last": "last_name", "bd": "birth_date", "pk": "id"}
>>> Person.objects.raw("SELECT * FROM some_other_table", translations=name_map)
```

## Index lookups

*raw()* supports indexing, so if you need only the first result you can write:

```python
>>> first_person = Person.objects.raw["SELECT * FROM myapp_person"](0)
```

However, the indexing and slicing are not performed at the database level. If you have a large number of Person objects in your database, it is more efficient to limit the query at the SQL level:

```python
>>> first_person = Person.objects.raw["SELECT * FROM myapp_person LIMIT 1"](0)
```

## Deferring Model Fields

Fields may also be left out:

```python
>>> people = Person.objects.raw("SELECT id, first_name FROM myapp_person")
```

The Person objects returned by this query will be deferred model instances (`see defer()`). This means that the fields that are omitted from the query will be loaded on demand. For example:

```python
>>> for p in Person.objects.raw("SELECT id, first_name FROM myapp_person"):
...     print(
...         p.first_name,
...         p.last_name,
...     )
...
John Smith
Jane Jones
```

***There is only one field that you can’t leave out - the primary key field. Django uses the primary key to identify model instances, so it must always be included in a raw query. A FieldDoesNotExist exception will be raised if you forget to include the primary key.***

## Adding annotations

You can also execute queries containing fields that aren’t defined on the model. For example, we could use PostgreSQL’s age() function to get a list of people with their ages calculated by the database:

```python
>>> people = Person.objects.raw("SELECT *, age(birth_date) AS age FROM myapp_person")
>>> for p in people:
...     print("%s is %s." % (p.first_name, p.age))
...
John is 37.
Jane is 42.
...
```

## Passing parameters into raw()

If you need to perform parameterized queries, you can use the params argument to raw():

```python
>>> lname = "Doe"
>>> Person.objects.raw("SELECT * FROM myapp_person WHERE last_name = %s", [lname])
```

params is a list or dictionary of parameters. You’ll use %s placeholders in the query string for a ***list, or %(key)s placeholders*** for a dictionary (where key is replaced by a dictionary key), regardless of your database engine. Such placeholders will be replaced with parameters from the params argument.

<i>Do not use string formatting on raw queries or quote placeholders in your SQL strings!

It’s tempting to write the above query as:

```python
>>> query = "SELECT * FROM myapp_person WHERE last_name = %s" % lname
>>> Person.objects.raw(query)
```

You might also think you should write your query like this (with quotes around %s):

```python
>>> query = "SELECT * FROM myapp_person WHERE last_name = '%s'"
```

<i>

## Executing custom SQL directly

Sometimes even Manager.raw() isn’t quite enough: you might need to perform queries that don’t map cleanly to models, or directly execute UPDATE, INSERT, or DELETE queries.

In these cases, you can always access the database directly, routing around the model layer entirely.

The object `django.db.connection` represents the default database connection. To use the database connection, call `connection.cursor()` to get a cursor object. Then, call `cursor.execute(sql, [params])` to execute the SQL and `cursor.fetchone()` or `cursor.fetchall()` to return the resulting rows.

```python
from django.db import connection

def my_custom_sql(self):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
        cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
        row = cursor.fetchone()

    return row
```

### More than one Database

if you are using more than one database, you can use django.db.connections to obtain the connection (and cursor) for a specific database. django.db.connections is a dictionary-like object that allows you to retrieve a specific connection using its alias:

```python
from django.db import connections

with connections["my_db_alias"].cursor() as cursor:
    # Your code here
    ...
```

By default, the Python DB API will return results without their field names, which means you end up with a list of values, rather than a dict. At a small performance and memory cost, you can return results as a dict by using something like this:

```python
def dictfetchall(cursor):
    """
    Return all rows from a cursor as a dict.
    Assume the column names are unique.
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
```

### SQL generated by Django's ORM

```python
In [18]: a = Question.objects.all()

In [19]: a
Out[19]: <QuerySet [<Question: What is your favorite color?>, <Question: Iron Man or Batman ?>, <Question: Better Villan ?>, <Question: Round Neck or Polo ?>, <Question: What is your favorite genre of music?>, <Question: Can you play any instruments?>, <Question: Who is you Favourite Superhero?>, <Question: Restaurent or Street Food ?>, <Question: Hello>, <Question: Film Industry ?>, <Question: Hello Kaise Ho ?>, <Question: Oneplus>, <Question: Desserts You Preffer>, <Question: How u Doin>, <Question: Do you prefer Zoom meetings or Slack messages?>, <Question: What is your favorite dessert?>, <Question: Batman or Iron Man ?>, <Question: What's New?>, <Question: What is your favorite cartoon?>, <Question: Favourite Desset ?>, '...(remaining elements truncated)...']>

In [20]: print(a.query)
SELECT "polls_question"."id", "polls_question"."created", "polls_question"."modified", "polls_question"."title", "polls_question"."description", "polls_question"."total_votes", "polls_question"."image", "polls_question"."tag_id" FROM "polls_question"
```

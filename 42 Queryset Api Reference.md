<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet" />

# QuerySet API reference

Internally, a QuerySet can be constructed, filtered, sliced, and generally passed around without actually hitting the database. No database activity actually occurs until you do something to evaluate the queryset.

## Iteration

A QuerySet is iterable, and it executes its database query the first time you iterate over it. For example, this will print the headline of all entries in the database:

```python
for e in Entry.objects.all():
    print(e.headline)
```

*Note: Don’t use this if all you want to do is determine if at least one result exists. It’s more efficient to use exists().*

## Asynchronous iteration

A QuerySet can also be iterated over using async for

```python
async for e in Entry.objects.all():
    results.append(e)
```

## Slicing

A QuerySet can be sliced, using Python’s array-slicing syntax. Slicing an unevaluated QuerySet usually returns another unevaluated QuerySet, but Django will execute the database query if you use the “step” parameter of slice syntax, and will return a list. Slicing a QuerySet that has been evaluated also returns a list

```python
In [18]: a = Question.objects.all()

In [19]: a
Out[19]: <QuerySet [<Question: What is your favorite color?>, <Question: Iron Man or Batman ?>, <Question: Better Villan ?>, <Question: Round Neck or Polo ?>, <Question: What is your favorite genre of music?>, <Question: Can you play any instruments?>, <Question: Who is you Favourite Superhero?>, <Question: Restaurent or Street Food ?>, <Question: Hello>, <Question: Film Industry ?>, <Question: Hello Kaise Ho ?>, <Question: Oneplus>, <Question: Desserts You Preffer>, <Question: How u Doin>, <Question: Do you prefer Zoom meetings or Slack messages?>, <Question: What is your favorite dessert?>, <Question: Batman or Iron Man ?>, <Question: What's New?>, <Question: What is your favorite cartoon?>, <Question: Favourite Desset ?>, '...(remaining elements truncated)...']>

In [20]: print(a.query)
SELECT "polls_question"."id", "polls_question"."created", "polls_question"."modified", "polls_question"."title", "polls_question"."description", "polls_question"."total_votes", "polls_question"."image", "polls_question"."tag_id" FROM "polls_question"

In [21]: print(type(a))
<class 'django.db.models.query.QuerySet'>

In [22]: b = Question.objects.all()[:10:2]

In [23]: b
Out[23]: 
[<Question: What is your favorite color?>,
 <Question: Better Villan ?>,
 <Question: What is your favorite genre of music?>,
 <Question: Who is you Favourite Superhero?>,
 <Question: Hello>]

In [24]: print(type(b))
<class 'list'>
```

### repr(). A QuerySet is evaluated when you call repr() on it. This is for convenience in the Python interactive interpreter, so you can immediately see your results when using the API interactively

### len(). A QuerySet is evaluated when you call len() on it. This, as you might expect, returns the length of the result list

*Note: If you only need to determine the number of records in the set (and don’t need the actual objects), it’s much more efficient to handle a count at the database level using SQL’s `SELECT COUNT(*)`. Django provides a count() method for precisely this reason.*

### list(). Force evaluation of a QuerySet by calling list() on it. For example

```python
entry_list = list(Entry.objects.all())
```

### bool(). Testing a QuerySet in a boolean context, such as using bool(), or, and or an if statement, will cause the query to be executed. If there is at least one result, the QuerySet is True, otherwise False. For example

```python
if Entry.objects.filter(headline="Test"):
    print("There is at least one Entry with the headline Test")
```

## Django ORM Methods

### 1. Filter

```python
filter(*args, **kwargs)
```

Returns a new QuerySet containing objects that match the given lookup parameters.

### 2. exclude()

```python
exclude(*args, **kwargs)
```

Returns a new QuerySet containing objects that do not match the given lookup parameters.

```python
Entry.objects.exclude(pub_date__gt=datetime.date(2005, 1, 3), headline="Hello")
```

In SQL terms, that evaluates to:

```sql
SELECT ...
WHERE NOT (pub_date > '2005-1-3' AND headline = 'Hello')
```

### 3. annotate()

```python
annotate(*args, **kwargs)
```

Annotates each object in the QuerySet with the provided list of query expressions. An expression may be a simple value, a reference to a field on the model (or any related models), or an aggregate expression (averages, sums, etc.) that has been computed over the objects that are related to the objects in the QuerySet.

```python
>>> from django.db.models import Count
>>> q = Blog.objects.annotate(Count("entry"))
# The name of the first blog
>>> q[0].name
'Blogasaurus'
# The number of entries on the first blog
>>> q[0].entry__count
42
```

The Blog model doesn’t define an entry__count attribute by itself, but by using a keyword argument to specify the aggregate function, you can control the name of the annotation:

```python
>>> q = Blog.objects.annotate(number_of_entries=Count("entry"))
>>>
# The number of entries on the first blog, using the name provided
>>>
>>> q[0].number_of_entries
42
```

### 4. alias()

```python
alias(*args, **kwargs)
```

Same as annotate(), but instead of annotating objects in the QuerySet, saves the expression for later reuse with other QuerySet methods. This is useful when the result of the expression itself is not needed but it is used for filtering, ordering, or as a part of a complex expression. Not selecting the unused value removes redundant work from the database which should result in better performance.

For example, if you want to find blogs with more than 5 entries, but are not interested in the exact number of entries, you could do this:

```python
>>> from django.db.models import Count
>>> blogs = Blog.objects.alias(entries=Count("entry")).filter(entries__gt=5)
```

alias() can be used in conjunction with annotate(), exclude(), filter(), order_by(), and update(). To use aliased expression with other methods (e.g. aggregate()), you must promote it to an annotation:

```python
Blog.objects.alias(entries=Count("entry")).annotate(
    entries=F("entries"),
).aggregate(Sum("entries"))
```

filter() and order_by() can take expressions directly, but expression construction and usage often does not happen in the same place (for example, QuerySet method creates expressions, for later use in views). alias() allows building complex expressions incrementally, possibly spanning multiple methods and modules, refer to the expression parts by their aliases and only use annotate() for the final result.

### 5. order_by()

```python
order_by(*fields)
```

By default, results returned by a QuerySet are ordered by the ordering tuple given by the ordering option in the model’s Meta. You can override this on a per-QuerySet basis by using the order_by method.

Example:

```python
Entry.objects.filter(pub_date__year=2005).order_by("-pub_date", "headline")
```

The result above will be ordered by pub_date descending, then by headline ascending. The negative sign in front of "-pub_date" indicates descending order. Ascending order is implied. To order randomly, use "?", like so:

```python
Entry.objects.order_by("?")
```

*Note: order_by('?') queries may be expensive and slow, depending on the database backend you’re using.*

To order by a field in a different model, use the same syntax as when you are querying across model relations. That is, the name of the field, followed by a double underscore (__), followed by the name of the field in the new model, and so on for as many models as you want to join. For example:

Entry.objects.order_by("blog__name", "headline")
If you try to order by a field that is a relation to another model, Django will use the default ordering on the related model, or order by the related model’s primary key if there is no Meta.ordering specified. For example, since the Blog model has no default ordering specified:

Entry.objects.order_by("blog")
…is identical to:

Entry.objects.order_by("blog__id")
If Blog had ordering = ['name'], then the first queryset would be identical to:

Entry.objects.order_by("blog__name")
You can also order by query expressions by calling asc() or desc() on the expression:

Entry.objects.order_by(Coalesce("summary", "headline").desc())
asc() and desc() have arguments (nulls_first and nulls_last) that control how null values are sorted.

Be cautious when ordering by fields in related models if you are also using distinct(). See the note in distinct() for an explanation of how related model ordering can change the expected results.

### 6. reverse()

```python
reverse()
```

Use the reverse() method to reverse the order in which a queryset’s elements are returned. Calling reverse() a second time restores the ordering back to the normal direction.

To retrieve the “last” five items in a queryset, you could do this:

```python
my_queryset.reverse()[:5]
```

### 7. distinct()

```python
distinct(*fields)
```

Returns a new QuerySet that uses SELECT DISTINCT in its SQL query. This eliminates duplicate rows from the query results.

By default, a QuerySet will not eliminate duplicate rows. In practice, this is rarely a problem, because simple queries such as Blog.objects.all() don’t introduce the possibility of duplicate result rows. However, if your query spans multiple tables, it’s possible to get duplicate results when a QuerySet is evaluated. That’s when you’d use distinct().

Examples

```python
>>> Author.objects.distinct()
[...]

>>> Entry.objects.order_by("pub_date").distinct("pub_date")
[...]

>>> Entry.objects.order_by("blog").distinct("blog")
[...]

>>> Entry.objects.order_by("author", "pub_date").distinct("author", "pub_date")
[...]

>>> Entry.objects.order_by("blog__name", "mod_date").distinct("blog__name", "mod_date")
[...]

>>> Entry.objects.order_by("author", "pub_date").distinct("author")
[...]
```

### 8. Values

```python
values(*fields, **expressions)
```

Returns a QuerySet that returns dictionaries, rather than model instances, when used as an iterable.

Each of those dictionaries represents an object, with the keys corresponding to the attribute names of model objects.

This example compares the dictionaries of values() with the normal model objects:

```python
# This list contains a Blog object
>>> Blog.objects.filter(name__startswith="Beatles")
<QuerySet [<Blog: Beatles Blog>]>

# This list contains a dictionary
>>> Blog.objects.filter(name__startswith="Beatles").values()
<QuerySet [{'id': 1, 'name': 'Beatles Blog', 'tagline': 'All the latest Beatles news.'}]>
```

The values() method takes optional positional arguments, *fields, which specify field names to which the SELECT should be limited.

```python
>>> Blog.objects.values()
<QuerySet [{'id': 1, 'name': 'Beatles Blog', 'tagline': 'All the latest Beatles news.'}]>
>>> Blog.objects.values("id", "name")
<QuerySet [{'id': 1, 'name': 'Beatles Blog'}]>
```

The values() method also takes optional keyword arguments, **expressions, which are passed through to annotate():

```python
>>> from django.db.models.functions import Lower
>>> Blog.objects.values(lower_name=Lower("name"))
<QuerySet [{'lower_name': 'beatles blog'}]>
```

*Finally, note that you can call `filter()`, `order_by()`, etc. after the values() call, that means that these two calls are identical:*

```python
Blog.objects.values().order_by("id")
Blog.objects.order_by("id").values()
```

### 9. values_list()

```python
values_list(*fields, flat=False, named=False)
```

This is similar to values() except that instead of returning dictionaries, it returns tuples when iterated over. Each tuple contains the value from the respective field or expression passed into the values_list() call — so the first item is the first field, etc. For example:

```python
>>> Entry.objects.values_list("id", "headline")
<QuerySet [(1, 'First entry'), ...]>
>>> from django.db.models.functions import Lower
>>> Entry.objects.values_list("id", Lower("headline"))
<QuerySet [(1, 'first entry'), ...]>
```

If you only pass in a single field, you can also pass in the flat parameter. If True, this will mean the returned results are single values, rather than 1-tuples. An example should make the difference clearer:

```python
>>> Entry.objects.values_list("id").order_by("id")
<QuerySet[(1,), (2,), (3,), ...]>

>>> Entry.objects.values_list("id", flat=True).order_by("id")
<QuerySet [1, 2, 3, ...]>
```

It is an error to pass in flat when there is more than one field.

You can pass named=True to get results as a namedtuple():

```python
>>> Entry.objects.values_list("id", "headline", named=True)
<QuerySet [Row(id=1, headline='First entry'), ...]>
```

### 10. dates()

```python
dates(field, kind, order='ASC')
```

Returns a QuerySet that evaluates to a list of datetime.date objects representing all available dates of a particular kind within the contents of the QuerySet.

field should be the name of a DateField of your model. kind should be either "year", "month", "week", or "day". Each datetime.date object in the result list is “truncated” to the given type.

- "year" returns a list of all distinct year values for the field.
- "month" returns a list of all distinct year/month values for the field.
- "week" returns a list of all distinct year/week values for the field. All dates will be a Monday.
- "day" returns a list of all distinct year/month/day values for the field.

Examples:

```python
>>> Entry.objects.dates("pub_date", "year")
[datetime.date(2005, 1, 1)]
>>> Entry.objects.dates("pub_date", "month")
[datetime.date(2005, 2, 1), datetime.date(2005, 3, 1)]
>>> Entry.objects.dates("pub_date", "week")
[datetime.date(2005, 2, 14), datetime.date(2005, 3, 14)]
>>> Entry.objects.dates("pub_date", "day")
[datetime.date(2005, 2, 20), datetime.date(2005, 3, 20)]
>>> Entry.objects.dates("pub_date", "day", order="DESC")
[datetime.date(2005, 3, 20), datetime.date(2005, 2, 20)]
>>> Entry.objects.filter(headline__contains="Lennon").dates("pub_date", "day")
[datetime.date(2005, 3, 20)]
```

### 11. datetimes()

```python
datetimes(field_name, kind, order='ASC', tzinfo=None)
```

Returns a QuerySet that evaluates to a list of datetime.datetime objects representing all available dates of a particular kind within the contents of the QuerySet.

field_name should be the name of a DateTimeField of your model.

kind should be either "year", "month", "week", "day", "hour", "minute", or "second". Each datetime.datetime object in the result list is “truncated” to the given type.

order, which defaults to 'ASC', should be either 'ASC' or 'DESC'. This specifies how to order the results.

### 12. none()

Calling none() will create a queryset that never returns any objects and no query will be executed when accessing the results. A qs.none() queryset is an instance of EmptyQuerySet.

Examples:

```python
>>> Entry.objects.none()
<QuerySet []>
>>> from django.db.models.query import EmptyQuerySet
>>> isinstance(Entry.objects.none(), EmptyQuerySet)
True
```

### 13. all()

Returns a copy of the current QuerySet (or QuerySet subclass). This can be useful in situations where you might want to pass in either a model manager or a QuerySet and do further filtering on the result. After calling all() on either object, you’ll definitely have a QuerySet to work with.

### 14. union()

```python
union(*other_qs, all=False)
```

Uses SQL’s UNION operator to combine the results of two or more QuerySets. For example:

```python
>>> qs1.union(qs2, qs3)
```

The UNION operator selects only distinct values by default. To allow duplicate values, use the all=True argument

### 15. intersection()

```python
intersection(*other_qs)
```

Uses SQL’s INTERSECT operator to return the shared elements of two or more QuerySets. For example:

```python
>>> qs1.intersection(qs2, qs3)
```

### 16. difference()

```python
difference(*other_qs)
```

Uses SQL’s EXCEPT operator to keep only elements present in the QuerySet but not in some other QuerySets. For example:

```python
>>> qs1.difference(qs2, qs3)
```

### 17. select_related()

```python
select_related(*fields)
```

Returns a QuerySet that will “follow” foreign-key relationships, selecting additional related-object data when it executes its query. This is a performance booster which results in a single more complex query but means later use of foreign-key relationships won’t require database queries.

The following examples illustrate the difference between plain lookups and select_related() lookups. Here’s standard lookup:

```python
# Hits the database
e = Entry.objects.get(id=5)
# Hits the database again to get the related Blog object
b = e.blog
```

And here’s select_related lookup:

```python
# Hits the database
e = Entry.objects.select_related("blog").get(id=5)
# Doesn't hit the database, because e.blog has been prepopulated
# in the previous query
b = e.blog
```

You can use select_related() with any queryset of objects:

```python
from django.utils import timezone

# Find all the blogs with entries scheduled to be published in the future
blogs = set()

for e in Entry.objects.filter(pub_date__gt=timezone.now()).select_related("blog"):
    # Without select_related(), this would make a database query for each
    # loop iteration in order to fetch the related blog for each entry.
    blogs.add(e.blog)
```

The order of filter() and select_related() chaining isn’t important. These querysets are equivalent:

```python
Entry.objects.filter(pub_date__gt=timezone.now()).select_related("blog")
Entry.objects.select_related("blog").filter(pub_date__gt=timezone.now())
```

You can follow foreign keys in a similar way to querying them. If you have the following models:

```python
from django.db import models

class City(models.Model):
    # ...
    pass

class Person(models.Model):
    # ...
    hometown = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

class Book(models.Model):
    # ...
    author = models.ForeignKey(Person, on_delete=models.CASCADE)
… then a call to Book.objects.select_related('author__hometown').get(id=4) will cache the related Person and the related City:

# Hits the database with joins to the author and hometown tables

b = Book.objects.select_related("author__hometown").get(id=4)
p = b.author  # Doesn't hit the database.
c = p.hometown  # Doesn't hit the database.

# Without select_related()

b = Book.objects.get(id=4)  # Hits the database.
p = b.author  # Hits the database.
c = p.hometown  # Hits the database.
```

You can refer to any ForeignKey or OneToOneField relation in the list of fields passed to select_related().
You can also refer to the reverse direction of a OneToOneField in the list of fields passed to select_related — that is, you can traverse a OneToOneField back to the object on which the field is defined. Instead of specifying the field name, use the related_name for the field on the related object.

There may be some situations where you wish to call select_related() with a lot of related objects, or where you don’t know all of the relations. In these cases it is possible to call select_related() with no arguments. This will follow all non-null foreign keys it can find - nullable foreign keys must be specified. This is not recommended in most cases as it is likely to make the underlying query more complex, and return more data, than is actually needed.

If you need to clear the list of related fields added by past calls of select_related on a QuerySet, you can pass None as a parameter:

```python
>>> without_relations = queryset.select_related(None)
```

Chaining select_related calls works in a similar way to other methods - that is that select_related('foo', 'bar') is equivalent to select_related('foo').select_related('bar').

```python
In [26]: c = Choice.objects.select_related("question__tag").get(id=1)

In [27]: c
Out[27]: <Choice: Not Much>

In [28]: c.question
Out[28]: <Question: What's New?>

In [29]: c.question.tag
Out[29]: <Tag: miscellaneous>
```

### 18, prefetch_related()¶

Returns a QuerySet that will automatically retrieve, in a single batch, related objects for each of the specified lookups.

```python
from django.db import models


class Topping(models.Model):
    name = models.CharField(max_length=30)


class Pizza(models.Model):
    name = models.CharField(max_length=50)
    toppings = models.ManyToManyField(Topping)

    def __str__(self):
        return "%s (%s)" % (
            self.name,
            ", ".join(topping.name for topping in self.toppings.all()),
        )
## and run:

>>> Pizza.objects.all()
["Hawaiian (ham, pineapple)", "Seafood (prawns, smoked salmon)"...
```

### 19. extra()¶

```python
extra(select=None, where=None, params=None, tables=None, order_by=None, select_params=None)¶
```

Sometimes, the Django query syntax by itself can’t easily express a complex WHERE clause. For these edge cases, Django provides the extra() QuerySet modifier — a hook for injecting specific clauses into the SQL generated by a QuerySet.

1. The select argument lets you put extra fields in the SELECT clause. It should be a dictionary mapping attribute names to SQL clauses to use to calculate that attribute.

```python
Blog.objects.extra(
    select={
        "entry_count": "SELECT COUNT(*) FROM blog_entry WHERE blog_entry.blog_id = blog_blog.id"
    },
)

```

Equivalent to Write

```sql
SELECT blog_blog.*, (SELECT COUNT(*) FROM blog_entry WHERE blog_entry.blog_id = blog_blog.id) AS entry_count
FROM blog_blog;
```

2. WHERE clauses - perhaps to perform non-explicit joins — by using where. You can manually add tables to the SQL FROM clause by using tables.

```python
Entry.objects.extra(where=["foo='a' OR bar = 'a'", "baz = 'a'"])
```

…translates (roughly) into the following SQL:

```sql
SELECT * FROM blog_entry WHERE (foo='a' OR bar='a') AND (baz='a')
```

3. ORDER BY - order the resulting queryset using some of the new fields or tables you have included via extra() use the order_by parameter to extra() and pass in a sequence of strings.

```python
q = Entry.objects.extra(select={"is_recent": "pub_date > '2006-01-01'"})
q = q.extra(order_by=["-is_recent"])
```

4. params - The where parameter described above may use standard Python database string placeholders — '%s' to indicate parameters the database engine should automatically quote. The params argument is a list of any extra parameters to be substituted.

Example:

Entry.objects.extra(where=["headline=%s"], params=["Lennon"])

### 20. select_for_update()¶

```python
select_for_update(nowait=False, skip_locked=False, of=(), no_key=False)
```

Returns a queryset that will lock rows until the end of the transaction, generating a SELECT ... FOR UPDATE SQL statement on supported databases.

For example:

```python
from django.db import transaction

entries = Entry.objects.select_for_update().filter(author=request.user)
with transaction.atomic():
    for entry in entries:
        ...
```

### 21 Operators That Return New Quesrysets

1. AND (&)

Combines two QuerySets using the SQL AND operator in a manner similar to chaining filters.

The following are equivalent:

```python
Model.objects.filter(x=1) & Model.objects.filter(y=2)
Model.objects.filter(x=1).filter(y=2)
```

SQL equivalent:

```sql
SELECT ... WHERE x=1 AND y=2
```

2. OR (|)

Combines two QuerySets using the SQL OR operator.

The following are equivalent:

```python
Model.objects.filter(x=1) | Model.objects.filter(y=2)
from django.db.models import Q

Model.objects.filter(Q(x=1) | Q(y=2))
```

SQL equivalent:

```sql
SELECT ... WHERE x=1 OR y=2
| is not a commutative operation, as different (though equivalent) queries may be generated.
```

## Methods That Return No Queryset

### 1. get

Returns the object matching the given lookup parameters, which should be in the format described in Field lookups. You should use lookups that are guaranteed unique, such as the primary key or fields in a unique constraint. For example:

```python
Entry.objects.get(id=1)
Entry.objects.get(Q(blog=blog) & Q(entry_number=1))
```

If get() doesn’t find any object, it raises a *Model.DoesNotExist* exception:

Entry.objects.get(id=-999)  # raises *Entry.DoesNotExist*
If get() finds more than one object, it raises a Model.MultipleObjectsReturned exception:

```python
Entry.objects.get(name="A Duplicated Name")  # raises Entry.MultipleObjectsReturned
```

### 2. create()

```python
create(**kwargs)
```

A convenience method for creating an object and saving it all in one step. Thus:

p = Person.objects.create(first_name="Bruce", last_name="Springsteen")
and:

p = Person(first_name="Bruce", last_name="Springsteen")
p.save(force_insert=True)

### 3. get_or_create()¶

A convenience method for looking up an object with the given kwargs (may be empty if your model has defaults for all fields), creating one if necessary.

Returns a tuple of (object, created), where object is the retrieved or created object and created is a boolean specifying whether a new object was created.

This is meant to prevent duplicate objects from being created when requests are made in parallel, and as a shortcut to boilerplatish code. For example:

```python
try:
    obj = Person.objects.get(first_name="John", last_name="Lennon")
except Person.DoesNotExist:
    obj = Person(first_name="John", last_name="Lennon", birthday=date(1940, 10, 9))
    obj.save()
```

Here, with concurrent requests, multiple attempts to save a Person with the same parameters may be made. To avoid this race condition, the above example can be rewritten using get_or_create() like so:

```python
obj, created = Person.objects.get_or_create(
    first_name="John",
    last_name="Lennon",
    defaults={"birthday": date(1940, 10, 9)},
)
```

### 4. update_or_create

A convenience method for updating an object with the given kwargs, creating a new one if necessary. Both create_defaults and defaults are dictionaries of (field, value) pairs. The values in both create_defaults and defaults can be callables. defaults is used to update the object while create_defaults are used for the create operation. If create_defaults is not supplied, defaults will be used for the create operation.

```python
defaults = {"first_name": "Bob"}
create_defaults = {"first_name": "Bob", "birthday": date(1940, 10, 9)}
try:
    obj = Person.objects.get(first_name="John", last_name="Lennon")
    for key, value in defaults.items():
        setattr(obj, key, value)
    obj.save()
except Person.DoesNotExist:
    new_values = {"first_name": "John", "last_name": "Lennon"}
    new_values.update(create_defaults)
    obj = Person(**new_values)
    obj.save()
```

This pattern gets quite unwieldy as the number of fields in a model goes up. The above example can be rewritten using update_or_create() like so:

```python
obj, created = Person.objects.update_or_create(
    first_name="John",
    last_name="Lennon",
    defaults={"first_name": "Bob"},
    create_defaults={"first_name": "Bob", "birthday": date(1940, 10, 9)},
)
```

### 5. bulk_create

This method inserts the provided list of objects into the database in an efficient manner (generally only 1 query, no matter how many objects there are), and returns created objects as a list, in the same order as provided:

```python
>>> objs = Entry.objects.bulk_create(
...     [
...         Entry(headline="This is a test"),
...         Entry(headline="This is only a test"),
...     ]
... )
```

### 6. bulk_update

This method efficiently updates the given fields on the provided model instances, generally with one query, and returns the number of objects updated:

```python
>>> objs = [
...     Entry.objects.create(headline="Entry 1"),
...     Entry.objects.create(headline="Entry 2"),
... ]
>>> objs[0].headline = "This is entry 1"
>>> objs[1].headline = "This is entry 2"
>>> Entry.objects.bulk_update(objs, ["headline"])
2
```

### 7. count

```python
# Returns the total number of entries in the database
Entry.objects.count()

# Returns the number of entries whose headline contains 'Lennon'
Entry.objects.filter(headline__contains="Lennon").count()
```

### 8. latest

This example returns the latest Entry in the table, according to the pub_date field:

```python
Entry.objects.latest("pub_date")
```

### 9. earliest

Works otherwise like latest() except the direction is changed.

### 10. first

Returns the first object matched by the queryset, or None if there is no matching object.

### 11. last

Works like first(), but returns the last object in the queryset.

### 12. aggregate

Returns a dictionary of aggregate values (averages, sums, etc.) calculated over the QuerySet. Each argument to aggregate() specifies a value that will be included in the dictionary that is returned

```python
>>> from django.db.models import Count
>>> Blog.objects.aggregate(Count("entry"))
{'entry__count': 16}
```

### 13. exists

Returns True if the QuerySet contains any results, and False if not. This tries to perform the query in the simplest and fastest way possible, but it does execute nearly the same query as a normal QuerySet query.

```python
if some_queryset.exists():
    print("There is at least one object in some_queryset")
```

### 14. contains

Returns True if the QuerySet contains obj, and False if not. This tries to perform the query in the simplest and fastest way possible.

```python
if some_queryset.contains(obj):
    print("Entry contained in queryset")
```

### 15 update

Performs an SQL update query for the specified fields, and returns the number of rows matched (which may not be equal to the number of rows updated if some rows already have the new value).

```python
>>> Entry.objects.filter(pub_date__year=2010).update(comments_on=False)
```

### 16. delete

Performs an SQL delete query on all rows in the QuerySet and returns the number of objects deleted and a dictionary with the number of deletions per object type

```python
>>> b = Blog.objects.get(pk=1)

# Delete all the entries belonging to this Blog
>>>
>>> Entry.objects.filter(blog=b).delete()
(4, {'blog.Entry': 2, 'blog.Entry_authors': 2})
```

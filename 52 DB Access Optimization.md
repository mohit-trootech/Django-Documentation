<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet"/>

# Django Database Optimization

Django’s database layer provides various ways to help developers get the most out of their databases. This document gathers together links to the relevant documentation, and adds various tips, organized under a number of headings that outline the steps to take when attempting to optimize your database usage.

## Cost Optimizatin Viewing

As general programming practice, this goes without saying. Find out what queries you are doing and what they are costing you. Use `QuerySet.explain()` to understand how specific QuerySets are executed by your database. You may also want to use an external project like `django-debug-toolbar`, or a tool that monitors your database directly.

## Indexes

```python
class IndexExample(models.Model):
    name = models.CharField(max_length=30, db_index=True)
    data = models.CharField(max_length=255, db_index=True)
    shortcut = models.CharField(max_length=7)
    edges = models.ManyToManyField(to="self")

    class Meta:
        indexes = [models.Index(fields=["shortcut"])]
```

## Querysets

To avoid performance problems, it is important to understand:

- QuerySets are lazy.
- when they are evaluated.
- how the data is held in memory.

### Lazy Querysets

QuerySets are lazy – the act of creating a QuerySet doesn’t involve any database activity. You can stack filters together all day long, and Django won’t actually run the query until the QuerySet is evaluated. Take a look at this example:

```python
>>> q = Entry.objects.filter(headline__startswith="What")
>>> q = q.filter(pub_date__lte=datetime.date.today())
>>> q = q.exclude(body_text__icontains="food")
>>> print(q)
```

Though this looks like three database hits, in fact it hits the database only once, at the last line *`print(q)`*. In general, the results of a QuerySet aren’t fetched from the database until you “ask” for them. When you do, the QuerySet is evaluated by accessing the database.

### When to Evaluate

Internally, a QuerySet can be constructed, filtered, sliced, and generally passed around without actually hitting the database. No database activity actually occurs until you do something to evaluate the queryset.

1. Iteration & Aysnc

```python
for e in Entry.objects.all():
print(e.title)
```

2. Slicing - [link](/42%20Queryset%20Api%20Reference.md)

3. Pickling - [link](/42%20Queryset%20Api%20Reference.md)

<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet" />

# Django Making Queries

Already Taked a Looked of some Django Making Queries like `get, filter & all` Now lets make some more advance queries. Also Try to Make Relavent SQL Queries.

### Sample Model

Through out this Module we will be Refering this sample model which we use later in our new project.

    from datetime import date

    from django.db import models

    class Blog(models.Model):
        name = models.CharField(max_length=100)
        tagline = models.TextField()

        def __str__(self):
            return self.name

    class Author(models.Model):
        name = models.CharField(max_length=200)
        email = models.EmailField()

        def __str__(self):
            return self.name

    class Entry(models.Model):
        blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
        headline = models.CharField(max_length=255)
        body_text = models.TextField()
        pub_date = models.DateField()
        mod_date = models.DateField(default=date.today)
        authors = models.ManyToManyField(Author)
        number_of_comments = models.IntegerField(default=0)
        number_of_pingbacks = models.IntegerField(default=0)
        rating = models.IntegerField(default=5)

        def __str__(self):
            return self.headline

# Queries

You can Start New Project Start a New App as we Dont Before and user django shell to access the models

*Note - Don't Forget to Migrate the models*

    python manage.py makemigrations
    python manage.py migrate
    python manage.py shell

## Creating Objects

To create an object, instantiate it using keyword arguments to the model class, then call `save()` to save it to the database.

    >>> from blog.models import Blog
    >>> b = Blog(name="Beatles Blog", tagline="All the latest Beatles news.")
    >>> b.save()

`.save()` method is used to create the object into database, But Instead you can use `create()` method to simple done this in one line.

    >>> p = Person.objects.create(first_name="Trever", last_name="Phillips")

## Updating Objects

To save changes to an object that’s already in the database, use save().

    >>> b.name = "New name"
    >>> b.save()

## Saving ForeignKey and ManyToManyField fields

Updating a ForeignKey field works exactly the same way as saving a normal field – assign an object of the right type to the field in question.

    >>> from blog.models import Blog, Entry
    >>> entry = Entry.objects.get(pk=1)
    >>> cheese_blog = Blog.objects.get(name="Cheddar Talk")
    >>> entry.blog = cheese_blog
    >>> entry.save()

Updating a ManyToManyField works a little differently – use the add() method on the field to add a record to the relation.

    >>> from blog.models import Author
    >>> joe = Author.objects.create(name="Joe")
    >>> entry.authors.add(joe)

To add multiple records to a ManyToManyField in one go, include multiple arguments in the call to add(),

    >>> john = Author.objects.create(name="John")
    >>> paul = Author.objects.create(name="Paul")
    >>> george = Author.objects.create(name="George")
    >>> ringo = Author.objects.create(name="Ringo")
    >>> entry.authors.add(john, paul, george, ringo)

## Retrieving Objects

1. Retrieving all Objects

The simplest way to retrieve objects from a table is to get all of them. To do this, use the all() method on a Manager:

    >>> all_entries = Entry.objects.all()
The all() method returns a QuerySet of all the objects in the database.

2. Retrieving specific objects with filters

To create such a subset, you refine the initial QuerySet, adding filter conditions.

- filter(**kwargs)
Returns a new QuerySet containing objects that match the given lookup parameters.

- exclude(**kwargs)
Returns a new QuerySet containing objects that do not match the given lookup parameters.

For example, to get a QuerySet of blog entries from the year 2006, use filter() like so:

    Entry.objects.filter(pub_date__year=2006)

### Chaining filters

The result of refining a QuerySet is itself a QuerySet, so it’s possible to chain refinements together. For example:

    >>> Entry.objects.filter(headline__startswith="What").exclude(
    ...     pub_date__gte=datetime.date.today()
    ... ).filter(pub_date__gte=datetime.date(2005, 1, 30))

### Filtered QuerySets are unique

Each time you refine a QuerySet, you get a brand-new QuerySet that is in no way bound to the previous QuerySet.

    >>> q1 = Entry.objects.filter(headline__startswith="What")
    >>> q2 = q1.exclude(pub_date__gte=datetime.date.today())
    >>> q3 = q1.filter(pub_date__gte=datetime.date.today())

### QuerySets are lazy

QuerySets are lazy – the act of creating a QuerySet doesn’t involve any database activity. You can stack filters together all day long, and Django won’t actually run the query until the QuerySet is evaluated. Take a look at this example:

    >>> q = Entry.objects.filter(headline__startswith="What")
    >>> q = q.filter(pub_date__lte=datetime.date.today())
    >>> q = q.exclude(body_text__icontains="food")
    >>> print(q)

Though this looks like three database hits, in fact it hits the database only once, at the last line (print(q)). In general, the results of a QuerySet aren’t fetched from the database until you “ask” for them.

## Retrieving a single object with get()

`filter()`will always give you a QuerySet, even if only a single object matches the query - in this case, it will be a QuerySet containing a single element.

If you know there is only one object that matches your query, you can use the `get()` method on a Manager which returns the object directly:

    >>> one_entry = Entry.objects.get(pk=1)

## Limiting QuerySets

Use a subset of Python’s array-slicing syntax to limit your QuerySet to a certain number of results. This is the equivalent of SQL’s LIMIT and OFFSET clauses.

For example, this returns the first 5 objects (LIMIT 5):

    >>> Entry.objects.all()[:5]
This returns the sixth through tenth objects (OFFSET 5 LIMIT 5):

    >>> Entry.objects.all()[5:10]
*Negative indexing (i.e. Entry.objects.all()[-1]) is not supported.*

Generally, slicing a QuerySet returns a new QuerySet – it doesn’t evaluate the query. An exception is if you use the “step” parameter of Python slice syntax. For example, this would actually execute the query in order to return a list of every second object of the first 10:

    >>> Entry.objects.all()[:10:2]
*Further filtering or ordering of a sliced queryset is prohibited due to the ambiguous nature of how that might work.*

To retrieve a single object rather than a list (e.g. SELECT foo FROM bar LIMIT 1), use an index instead of a slice. For example, this returns the first Entry in the database, after ordering entries alphabetically by headline:

    >>> Entry.objects.order_by["headline"](0)
This is roughly equivalent to:

    >>> Entry.objects.order_by["headline"](0:1).get()
*Note, however, that the first of these will raise IndexError while the second will raise DoesNotExist if no objects match the given criteria. See `get()` for more details.*

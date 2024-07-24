<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet" />

# Field lookups

Field lookups are how you specify the meat of an SQL WHERE clause. They’re specified as keyword arguments to the QuerySet methods filter(), exclude() and get().

Basic lookups keyword arguments take the form `field__lookuptype=value`. (That’s a double-underscore).

## __lte

less than equals to `__lte`

    Entry.objects.filter(pub_date__lte="2006-01-01")
translates (roughly) into the following SQL:

    SELECT * FROM blog_entry WHERE pub_date <= '2006-01-01';

- *Similar __gte (greater than equals to can be used)*

### __gt

greater than `__gt`

    Entry.objects.filter(pub_date__gt="2006-01-01")
translates (roughly) into the following SQL:

    SELECT * FROM blog_entry WHERE pub_date > '2006-01-01';

- *Similar __lt (less than can be used)*

## __exact

An “exact” match.

    >>> Entry.objects.get(headline__exact="Cat bites dog")
Would generate SQL along these lines:

    SELECT entrys WHERE headline = 'Cat bites dog';

## __iexact

A case-insensitive match. So, the query:

    >>> Blog.objects.get(name__iexact="beatles blog")
Would match a Blog titled "Beatles Blog", "beatles blog", or even "BeAtlES blOG".

## contain

Case-sensitive containment test. For example:

    Entry.objects.get(headline__contains="Lennon")
Roughly translates to this SQL:

    SELECT ... WHERE headline LIKE '%Lennon%';
Note this will match the headline 'Today Lennon honored' but not 'today lennon honored'.

*There’s also a case-insensitive version, icontains.*

## startswith, endswith

Starts-with and ends-with search, respectively. There are also case-insensitive versions called istartswith and iendswith.
Again, this only scratches the surface. A complete reference can be found in the field lookup reference.

    >>> Entry.objects.filter(headline__startswith="What")

Returns all the data whose headline starts with `What`, Similarly for endswith,

    >>> Entry.objects.filter(headline__endswith="What")

Return all the data which ends with `what`

- *Note - Similar incase sensitive lookup is also available, `__istartswith, __iendswith`*

## Lookups with Relationships

Django offers a powerful and intuitive way to “follow” relationships in lookups, taking care of the SQL JOINs for you automatically, behind the scenes. To span a relationship, use the field name of related fields across models, separated by double underscores, until you get to the field you want.

This example retrieves all Entry objects with a Blog whose name is 'Beatles Blog':

    >>> Entry.objects.filter(blog__name="Beatles Blog")

This example retrieves all Blog objects which have at least one Entry whose headline contains 'Lennon':

    >>> Blog.objects.filter(entry__headline__contains="Lennon")

More Examples,

    >>> Blog.objects.filter(entry__authors__name="Lennon")
    >>> Blog.objects.filter(entry__authors__name__isnull=True)
    >>> Blog.objects.filter(entry__authors__isnull=False, entry__authors__name__isnull=True)

## Multivalued Relationships

To select all blogs containing at least one entry from 2008 having “Lennon” in its headline (the same entry satisfying both conditions), we would write:

    >>> Blog.objects.filter(entry__headline__contains="Lennon", entry__pub_date__year=2008)

## Models Filtering

Find a list of all blog entries that have had more comments than pingbacks, we construct an F() object to reference the pingback count, and use that F() object in the query:

    >>> from django.db.models import F
    >>> Entry.objects.filter(number_of_comments__gt=F("number_of_pingbacks"))

# Comparing Objects

To compare two model instances, use the standard Python comparison operator, the double equals sign: ==. Behind the scenes, that compares the primary key values of two models.

Using the Entry example above, the following two statements are equivalent:

    >>> some_entry == other_entry
    >>> some_entry.id == other_entry.id
If a model’s primary key isn’t called id, no problem. Comparisons will always use the primary key, whatever it’s called. For example, if a model’s primary key field is called name, these two statements are equivalent:

    >>> some_obj == other_obj
    >>> some_obj.name == other_obj.name

## Deleting objects

The delete method, conveniently, is named delete(). This method immediately deletes the object and returns the number of objects deleted and a dictionary with the number of deletions per object type. Example:

    >>> e.delete()
    (1, {'blog.Entry': 1})
You can also delete objects in bulk. Every QuerySet has a delete() method, which deletes all members of that QuerySet.

For example, this deletes all Entry objects with a pub_date year of 2005:

    >>> Entry.objects.filter(pub_date__year=2005).delete()
    (5, {'webapp.Entry': 5})

- *No Roll back After Delete*

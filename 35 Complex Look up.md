<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet" />

# Complex lookups with Q objects

Ever Think of Subqueries in SQl, Right But How to Implement Subqueries in Django, `Q` objects lookup execute more complex queries (for example, queries with OR statements).
A Q object (django.db.models.Q) is an object used to encapsulate a collection of keyword arguments.

For example, this Q object encapsulates a single LIKE query:

    from django.db.models import Q

    Q(question__startswith="What")
Q objects can be combined using the &, |, and ^ operators. When an operator is used on two Q objects, it yields a new Q object.

For example, this statement yields a single Q object that represents the “OR” of two "question__startswith" queries:

    Q(question__startswith="Who") | Q(question__startswith="What")

This is equivalent to the following SQL WHERE clause:

    WHERE question LIKE 'Who%' OR question LIKE 'What%'
You can compose statements of arbitrary complexity by combining Q objects with the &, |, and ^ operators and use parenthetical grouping.

Also, Q objects can be negated using the ~ operator, allowing for combined lookups that combine both a normal query and a negated (NOT) query:

    Q(question__startswith="Who") | ~Q(pub_date__year=2005)

Lets Understand with Some Polls Examples,

    Poll.objects.get(
        Q(question__startswith="Who"),
        Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6)),
    )

Equivalent to,

    SELECT * from polls WHERE question LIKE 'Who%'
        AND (pub_date = '2005-05-02' OR pub_date = '2005-05-06')

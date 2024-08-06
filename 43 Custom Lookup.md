<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet" />

# Custom Lookup

We will write a custom lookup ne which works opposite to exact. Author.objects.filter(name__ne='Jack') will translate to the SQL:

    ***"author"."name" <> 'Jack'***

```python
from django.db.models import Lookup


class NotEqual(Lookup):
    lookup_name = "ne"

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return "%s <> %s" % (lhs, rhs), params
```

## Transform Examples

The custom lookup above is great, but in some cases you may want to be able to chain lookups together. For example, let’s suppose we are building an application where we want to make use of the abs() operator. We have an Experiment model which records a start value, end value, and the change (start - end). We would like to find all experiments where the change was equal to a certain amount

We will start by writing an AbsoluteValue transformer. This will use the SQL function ABS() to transform the value before comparison:

```python
from django.db.models import Transform

class AbsoluteValue(Transform):
    lookup_name = "abs"
    function = "ABS"
```

***Next, let’s register it for IntegerField***

```python
@Field.register_lookup
class AbsoluteValueLessThan(Lookup):
    lookup_name = "lt"

    def as_sql(self, compiler, connection):
        lhs, lhs_params = compiler.compile(self.lhs.lhs)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params + lhs_params + rhs_params
        return "%s < %s AND %s > -%s" % (lhs, rhs, lhs, rhs), params

@Field.register_lookup
class MySQLNotEqual(NotEqual):
    def as_mysql(self, compiler, connection, **extra_context):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return "%s != %s" % (lhs, rhs), params
```

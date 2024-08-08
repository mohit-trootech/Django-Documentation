<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet"/>

# View decorators

Django provides several decorators that can be applied to views to support various HTTP features.

## Allowed HTTP methods

The decorators in `django.views.decorators.http` can be used to restrict access to views based on the request method. These decorators will return a `django.http.HttpResponseNotAllowed` if the conditions are not met.

### 1. require_http_methods(request methods list)

Decorator to require that a view only accepts particular request methods

```python
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET", "POST"]) <- Request Methods should be uppercase
def my_view(request):
    # I can assume now that only GET or POST requests make it this far
    # ...
    pass
```

***Note that request methods should be in uppercase.***

1. request_GET() - Decorator for accept GET method only.
2. request_POST() - Decorator for accept POST method only.
3. request_safe() - Decorator to require that a view only accepts the GET and HEAD methods. These methods are commonly considered “safe” because they should not have the significance of taking an action other than retrieving the requested resource.

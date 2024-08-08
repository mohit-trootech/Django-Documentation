<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet"/>

# django.urls utility functions

## reverse()

If you need to use something similar to the url template tag in your code, Django provides the following function:

```python
reverse(viewname, urlconf=None, args=None, kwargs=None, current_app=None)
```

viewname can be a URL pattern name or the callable view object. For example, given the following url:

```python
from news import views

path("archive/", views.archive, name="news-archive")
```

you can use any of the following to reverse the URL:

```python
# using the named URL

reverse("news-archive")

# passing a callable object

# (This is discouraged because you can't reverse namespaced views this way.)

from news import views

reverse(views.archive)
```

If the URL accepts arguments, you may pass them in args. For example:
from django.urls import reverse

```python
def myview(request):
    return HttpResponseRedirect(reverse("arch-summary", args=[1945]))
You can also pass kwargs instead of args. For example:

>>> reverse("admin:app_list", kwargs={"app_label": "auth"})
'/admin/auth/'
```

args and kwargs cannot be passed to reverse() at the same time.

If no match can be made, reverse() raises a NoReverseMatch exception.

The reverse() function can reverse a large variety of regular expression patterns for URLs, but not every possible one. The main restriction at the moment is that the pattern cannot contain alternative choices using the vertical bar ("|") character. You can quite happily use such patterns for matching against incoming URLs and sending them off to views, but you cannot reverse such patterns.

## reverse_lazy()

A lazily evaluated version of reverse().

```python
reverse_lazy(viewname, urlconf=None, args=None, kwargs=None, current_app=None)
```

It is useful for when you need to use a URL reversal before your project’s URLConf is loaded. Some common cases where this function is necessary are:

1. 0providing a reversed URL as the url attribute of a generic class-based view.
2. providing a reversed URL to a decorator (such as the login_url argument for the django.contrib.auth.decorators.permission_required() decorator).
3. providing a reversed URL as a default value for a parameter in a function’s signature.

## resolve()

The resolve() function can be used for resolving URL paths to the corresponding view functions. It has the following signature:

```python
resolve(path, urlconf=None)
```

path is the URL path you want to resolve. As with reverse(), you don’t need to worry about the urlconf parameter. The function returns a ResolverMatch object that allows you to access various metadata about the resolved URL.

If the URL does not resolve, the function raises a Resolver404 exception (a subclass of Http404) .

```python
class ResolverMatch
func
The view function that would be used to serve the URL

args
The arguments that would be passed to the view function, as parsed from the URL.

kwargs
All keyword arguments that would be passed to the view function, i.e. captured_kwargs and extra_kwargs.

captured_kwargs
The captured keyword arguments that would be passed to the view function, as parsed from the URL.

extra_kwargs
The additional keyword arguments that would be passed to the view function.

url_name
The name of the URL pattern that matches the URL.

route
The route of the matching URL pattern.

For example, if path('users/<id>/', ...) is the matching pattern, route will contain 'users/<id>/'.

tried
The list of URL patterns tried before the URL either matched one or exhausted available patterns.

app_name
The application namespace for the URL pattern that matches the URL.

app_names
The list of individual namespace components in the full application namespace for the URL pattern that matches the URL. For example, if the app_name is 'foo:bar', then app_names will be ['foo', 'bar'].

namespace
The instance namespace for the URL pattern that matches the URL.

namespaces
The list of individual namespace components in the full instance namespace for the URL pattern that matches the URL. i.e., if the namespace is foo:bar, then namespaces will be ['foo', 'bar'].

view_name
The name of the view that matches the URL, including the namespace if there is one.
```

A ResolverMatch object can then be interrogated to provide information about the URL pattern that matches a URL:

```python
In [32]: url = resolve("/polls/")

In [33]: url
Out[33]: ResolverMatch(func=polls.views.IndexView, args=(), kwargs={}, url_name='index', app_names=[], namespaces=[], route='polls/')

In [34]: url.func
Out[34]: <function polls.views.View.as_view.<locals>.view(request, *args, **kwargs)>

In [35]: url.args
Out[35]: ()

In [36]: url.url_name
Out[36]: 'index'

In [37]: url.route
Out[37]: 'polls/'

In [38]: url.tried
Out[38]:
[[<URLPattern '' [name='home']>],
 [<URLResolver <module 'learning.urls' from '/home/trootech/Mohit/Django-Documentation/mysite/learning/urls.py'> (None:None) 'learn/'>],
 [<URLResolver <module 'polls.urls' from '/home/trootech/Mohit/Django-Documentation/mysite/polls/urls.py'> (None:None) 'polls/'>,
  <URLPattern '' [name='index']>]]

In [39]: url.app_name
Out[39]: ''

In [40]: url.app_names
Out[40]: []

In [41]: url.namespace
Out[41]: ''

In [42]: url.view_name
Out[42]: 'index'
```

Another Example

```python
# Resolve a URL

match = resolve("/some/path/")

# Print the URL pattern that matches the URL

print(match.url_name)
A ResolverMatch object can also be assigned to a triple:

func, args, kwargs = resolve("/some/path/")
One possible use of resolve() would be to test whether a view would raise a Http404 error before redirecting to it:

from urllib.parse import urlparse
from django.urls import resolve
from django.http import Http404, HttpResponseRedirect

def myview(request):
    next = request.META.get("HTTP_REFERER", None) or "/"
    response = HttpResponseRedirect(next)

    # modify the request and response as required, e.g. change locale
    # and set corresponding locale cookie

    view, args, kwargs = resolve(urlparse(next)[2])
    kwargs["request"] = request
    try:
        view(*args, **kwargs)
    except Http404:
        return HttpResponseRedirect("/")
    return response
```

## get_script_prefix()

```python
get_script_prefix()
```

Normally, you should always use `reverse()` to define URLs within your application. However, if your application constructs part of the URL hierarchy itself, you may occasionally need to generate URLs. In that case, you need to be able to find the base URL of the Django project within its web server (normally, `reverse()` takes care of this for you). In that case, you can call get_script_prefix(), which will return the script prefix portion of the URL for your Django project. If your Django project is at the root of its web server, this is always `"/"`.

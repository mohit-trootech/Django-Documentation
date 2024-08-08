<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet"/>

# django.urls Function for use in URL Config

## path()

```python
path(route, view, kwargs=None, name=None)
```

Returns an element for inclusion in urlpatterns. For example:

```python
from django.urls import include, path

urlpatterns = [
    path("index/", views.index, name="main-view"),
    path("bio/<username>/", views.bio, name="bio"),
    path("articles/<slug:title>/", views.article, name="article-detail"),
    path("articles/<slug:title>/<int:section>/", views.section, name="article-section"),
    path("blog/", include("blog.urls")),
    ...,
]
```

The route argument should be a string or gettext_lazy() to capture part of the URL and send it as a keyword argument to the view.

The view argument is a view function or the result of as_view() for class-based views. It can also be an `django.urls.include()`.

The kwargs argument allows you to pass additional arguments to the view function or method. See Passing extra options to view functions for an example.

## re_path()

```python
re_path(route, view, kwargs=None, name=None)
```

Returns an element for inclusion in urlpatterns. For example:

```python
from django.urls import include, re_path

urlpatterns = [
    re_path(r"^index/$", views.index, name="index"),
    re_path(r"^bio/(?P<username>\w+)/$", views.bio, name="bio"),
    re_path(r"^blog/", include("blog.urls")),
    ...,
]
```

The route argument should be a string or gettext_lazy() (see Translating URL patterns) that contains a regular expression compatible with Python’s re module. Strings typically use raw string syntax (r'') so that they can contain sequences like \d without the need to escape the backslash with another backslash. When a match is made, captured groups from the regular expression are passed to the view – as named arguments if the groups are named, and as positional arguments otherwise. The values are passed as strings, without any type conversion.

When a route ends with $ the whole requested URL, matching against path_info, must match the regular expression pattern (re.fullmatch() is used).

## include()

```python
include(module, namespace=None)
include(pattern_list)
include((pattern_list, app_namespace), namespace=None)
```

A function that takes a full Python import path to another URLconf module that should be “included” in this place. Optionally, the application namespace and instance namespace where the entries will be included into can also be specified.

## register_converter()

```python
register_converter(converter, type_name)
```

The function for registering a converter for use in path() routes.

For example:

```python

class FourDigitYearConverter:
    regex = "[0-9]{4}"

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return "%04d" % value
Register custom converter classes in your URLconf using register_converter():

from django.urls import path, register_converter

from . import converters, views

register_converter(converters.FourDigitYearConverter, "yyyy")

urlpatterns = [
    path("articles/2003/", views.special_case_2003),
    path("articles/<yyyy:year>/", views.year_archive),
    ...,
]
```

## static()

```python
static.static(prefix, view=django.views.static.serve, **kwargs)
```

Helper function to return a URL pattern for serving files in debug mode:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... the rest of your URLconf goes here ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## handler400

A callable, or a string representing the full Python import path to the view that should be called if the HTTP client has sent a request that caused an error condition and a response with a status code of 400.

By default, this is django.views.defaults.bad_request(). If you implement a custom view, be sure it accepts request and exception arguments and returns an HttpResponseBadRequest.

## handler403

A callable, or a string representing the full Python import path to the view that should be called if the user doesn’t have the permissions required to access a resource.

By default, this is django.views.defaults.permission_denied(). If you implement a custom view, be sure it accepts request and exception arguments and returns an HttpResponseForbidden.

## handler404

A callable, or a string representing the full Python import path to the view that should be called if none of the URL patterns match.

By default, this is django.views.defaults.page_not_found(). If you implement a custom view, be sure it accepts request and exception arguments and returns an HttpResponseNotFound.

## handler500

A callable, or a string representing the full Python import path to the view that should be called in case of server errors. Server errors happen when you have runtime errors in view code.

By default, this is django.views.defaults.server_error(). If you implement a custom view, be sure it accepts a request argument and returns an HttpResponseServerError.

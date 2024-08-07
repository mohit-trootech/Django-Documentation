<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet"/>

# URL Dispatcher

To design URLs for an app, you create a Python module informally called a URLconf (URL configuration). This module is pure Python code and is a mapping between URL path expressions to Python functions (your views).

```python
from django.urls import path

from . import views

urlpatterns = [
    path("articles/2003/", views.special_case_2003),
    path("articles/<int:year>/", views.year_archive),
    path("articles/<int:year>/<int:month>/", views.month_archive),
    path("articles/<int:year>/<int:month>/<slug:slug>/", views.article_detail),
]
```

## How Django Process Request

When a user requests a page from your Django-powered site, this is the algorithm the system follows to determine which Python code to execute:

### 1. ROOT_URLCONF

Django determines the root URLconf module to use. Ordinarily, this is the value of the ROOT_URLCONF setting, but if the incoming HttpRequest object has a urlconf attribute (set by middleware), its value will be used in place of the ROOT_URLCONF setting

```python
ROOT_URLCONF = "mysite.urls"
```

### 2. Url Pattern

Django loads that Python module and looks for the variable urlpatterns. This should be a sequence of `django.urls.path()` and/or `django.urls.re_path()` instances.

```python
urlpatterns = [
    path("", RedirectView.as_view(url="/polls"), name="home"),
    # path("", InputForm.as_view(), name="form"),
    path("polls/", include("polls.urls")),
    path("accounts/", include("accounts.urls")),
    path("admin/", admin.site.urls),
    path("schema/", Schema.as_view()),
] + debug_toolbar_urls()
```

### 3. Url Patten Matching

Django runs through each URL pattern, in order, and stops at the first one that matches the requested URL, matching against path_info.

### 4. Patten Match

Once one of the URL patterns matches, Django imports and calls the given view, which is a Python function (or a class-based view). The view gets passed the following arguments:

1. An instance of HttpRequest.
2. If the matched URL pattern contained no named groups, then the matches from the regular expression are provided as positional arguments.
3. The keyword arguments are made up of any named parts matched by the path expression that are provided, overridden by any arguments specified in the optional kwargs argument to *`django.urls.path()`* or *`django.urls.re_path()`*.

### 5. No URL Match Exception Case

If no URL pattern matches, or if an exception is raised during any point in this process, Django invokes an appropriate error-handling view. See Error handling below.

## Path Converters

The following path converters are available by default:

1. str - Matches any non-empty string, excluding the path separator, '/'. This is the default if a converter isn’t included in the expression.
2. int - Matches zero or any positive integer. Returns an int.
3. slug - Matches any slug string consisting of ASCII letters or numbers, plus the hyphen and underscore characters. For example, `building-your-1st-django-site`.
4. uuid - Matches a formatted UUID. To prevent multiple URLs from mapping to the same page, dashes must be included and letters must be lowercase. For example, `075194d3-6885-417e-a8a8-6c931e272f00`/ Returns a UUID instance.
5. path - Matches any non-empty string, including the path separator, '/'. This allows you to match against a complete URL path rather than a segment of a URL path as with str.

## Error Handling

When Django can’t find a match for the requested URL, or when an exception is raised, Django invokes an error-handling view.

The views to use for these cases are specified by four variables. Their default values should suffice for most projects, but further customization is possible by overriding their default values.

See the documentation on customizing error views for the full details.

Such values can be set in your root URLconf. Setting these variables in any other URLconf will have no effect.

Values must be callables, or strings representing the full Python import path to the view that should be called to handle the error condition at hand.

The variables are:

### 1. handler400

A callable, or a string representing the full Python import path to the view that should be called if the HTTP client has sent a request that caused an error condition and a response with a status code of 400.

### 2. handler403

A callable, or a string representing the full Python import path to the view that should be called if the user doesn’t have the permissions required to access a resource.

### 3. handler404

A callable, or a string representing the full Python import path to the view that should be called if none of the URL patterns match.

### 4. handler500

A callable, or a string representing the full Python import path to the view that should be called in case of server errors. Server errors happen when you have runtime errors in view code.

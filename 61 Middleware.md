<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet"/>

# Middleware

Middleware is a framework of hooks into Django’s request/response processing. It’s a light, low-level “plugin” system for globally altering Django’s input or output.

Middleware in Django serves as a critical component in the request-response cycle. It's a framework of hooks that process requests and responses, acting before and after view functions. Middleware can alter the request and response objects, query data, handle sessions or cookies, and redirect or modify the execution flow.

When a request is made to a Django server, it doesn't directly reach the view. Instead, it passes through various middleware layers defined in settings.py under MIDDLEWARE. Each Django middleware layer can perform actions before passing the request to the next layer or the view.

```python
MIDDLEWARE = [
   'django.middleware.security.SecurityMiddleware',
   'django.contrib.sessions.middleware.SessionMiddleware',
   'django.middleware.common.CommonMiddleware',
   'django.middleware.csrf.CsrfViewMiddleware',
   'django.contrib.auth.middleware.AuthenticationMiddleware',
   'django.contrib.messages.middleware.MessageMiddleware',
   'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

Here’s what each Django middleware layer does:

1. SecurityMiddleware enhances security by adding headers like X-XSS-Protection, X-Content-Type-Options, and enforcing SSL/TLS (HTTPS) and other security-related settings.

2. SessionMiddleware manages sessions across requests, enabling the use of session framework, which stores data on a per-site-visitor basis.

3. CommonMiddleware provides various functionalities, such as URL redirections, appending trailing slashes, and sending 404 errors for missing favicon.ico requests.

4. CsrfViewMiddleware adds Cross-Site Request Forgery protection to your forms by checking for a special token in each POST request.

5. AuthenticationMiddleware associates users with requests using sessions, making the request.user attribute available in view functions.

6. MessageMiddleware enables temporary message storage, allowing one-time display messages to be passed between views.

7. XFrameOptionsMiddleware provides clickjacking protection by setting the X-Frame-Options HTTP header, which controls whether a browser should allow a page to be rendered in a *`<frame>, <iframe>, <embed>, or <object>.`*

After the view processes the request, the response goes through the middleware layers in reverse order, allowing further manipulation.

## Writing your own middleware

A middleware factory is a callable that takes a get_response callable and returns a middleware. A middleware is a callable that takes a request and returns a response, just like a view.

> A Middleware Function can be Written as a function that looks like this:

```python
def simple_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware
```

> OR Class Based Implmentation

```python
class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
```

## Activating Middleware

To activate a middleware component, add it to the MIDDLEWARE list in your Django settings.

In MIDDLEWARE, each middleware component is represented by a string: the full Python path to the middleware factory’s class or function name. For example, here’s the default value created by django-admin startproject:

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
```

## Other Middleware Hooks

Besides the basic request/response middleware pattern described earlier, you can add three other special methods to class-based middleware:

### process_view()

```python
process_view(request, view_func, view_args, view_kwargs)
```

request is an HttpRequest object. view_func is the Python function that Django is about to use. (It’s the actual function object, not the name of the function as a string.) view_args is a list of positional arguments that will be passed to the view, and view_kwargs is a dictionary of keyword arguments that will be passed to the view. Neither view_args nor view_kwargs include the first view argument (request).

process_view() is called just before Django calls the view.

It should return either None or an HttpResponse object. If it returns None, Django will continue processing this request, executing any other process_view() middleware and, then, the appropriate view. If it returns an HttpResponse object, Django won’t bother calling the appropriate view; it’ll apply response middleware to that HttpResponse and return the result.

### process_exception()

```python
process_exception(request, exception)
```

request is an HttpRequest object. exception is an Exception object raised by the view function.

Django calls process_exception() when a view raises an exception. process_exception() should return either None or an HttpResponse object. If it returns an HttpResponse object, the template response and response middleware will be applied and the resulting response returned to the browser. Otherwise, default exception handling kicks in.

Again, middleware are run in reverse order during the response phase, which includes process_exception. If an exception middleware returns a response, the process_exception methods of the middleware classes above that middleware won’t be called at all.

### process_template_response()

```python
process_template_response(request, response)
```

request is an HttpRequest object. response is the TemplateResponse object (or equivalent) returned by a Django view or by a middleware.

process_template_response() is called just after the view has finished executing, if the response instance has a render() method, indicating that it is a TemplateResponse or equivalent.

It must return a response object that implements a render method. It could alter the given response by changing response.template_name and response.context_data, or it could create and return a brand-new TemplateResponse or equivalent.

You don’t need to explicitly render responses – responses will be automatically rendered once all template response middleware has been called.

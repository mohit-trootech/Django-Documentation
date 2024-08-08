<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet"/>

# Request and response objects

When a page is requested, Django creates an HttpRequest object that contains metadata about the request. Then Django loads the appropriate view, passing the HttpRequest as the first argument to the view function. Each view is responsible for returning an HttpResponse object.

## Http Request Object

```python
class HttpRequest
```

### Attributes

All attributes should be considered read-only, unless stated otherwise.

#### 1. Request.scheme

A string representing the scheme of the request (*`http`* or *`https`* usually).

#### 2. HttpRequest.body

The raw HTTP request body as a bytestring. This is useful for processing data in different ways than conventional HTML forms: binary images, XML payload etc. For processing conventional form data, use HttpRequest.POST.

You can also read from an HttpRequest using a file-like interface with HttpRequest.read() or HttpRequest.readline(). Accessing the body attribute after reading the request with either of these I/O stream methods will produce a RawPostDataException.

#### 3. HttpRequest.path

A string representing the full path to the requested page, not including the scheme, domain, or query string.

```bash
Example: "/music/bands/the_beatles/"
```

#### 4. HttpRequest.path_info

Under some web server configurations, the portion of the URL after the host name is split up into a script prefix portion and a path info portion. The path_info attribute always contains the path info portion of the path, no matter what web server is being used. Using this instead of path can make your code easier to move between test and deployment servers.

For example, if the `WSGIScriptAlias` for your application is set to `"/minfo"`, then path might be `"/minfo/music/bands/the_beatles/"` and path_info would be `"/music/bands/the_beatles/"`.

#### 5. HttpRequest.method

A string representing the HTTP method used in the request. This is guaranteed to be uppercase. For example:

```python
if request.method == "GET":
    do_something()
elif request.method == "POST":
    do_something_else()
```

#### 6. HttpRequest.encoding

A string representing the current encoding used to decode form submission data (or None, which means the DEFAULT_CHARSET setting is used). You can write to this attribute to change the encoding used when accessing the form data. Any subsequent attribute accesses (such as reading from GET or POST) will use the new encoding value. Useful if you know the form data is not in the DEFAULT_CHARSET encoding.

#### 7. HttpRequest.content_type

A string representing the MIME type of the request, parsed from the CONTENT_TYPE header.

#### 8. HttpRequest.content_params

A dictionary of key/value parameters included in the CONTENT_TYPE header.

#### 9. HttpRequest.GET

A dictionary-like object containing all given HTTP GET parameters. See the QueryDict documentation below.

#### 10. HttpRequest.POST

A dictionary-like object containing all given HTTP POST parameters, providing that the request contains form data. See the QueryDict documentation below. If you need to access raw or non-form data posted in the request, access this through the HttpRequest.body attribute instead.

It’s possible that a request can come in via POST with an empty POST dictionary – if, say, a form is requested via the POST HTTP method but does not include form data. Therefore, you shouldn’t use if request.POST to check for use of the POST method; instead, use if request.method == "POST" (see HttpRequest.method).

POST does not include file-upload information. See FILES.

#### 11. HttpRequest.COOKIES

A dictionary containing all cookies. Keys and values are strings.

#### 12. HttpRequest.FILES

A dictionary-like object containing all uploaded files. Each key in FILES is the name from the `<input type="file" name="">`. Each value in FILES is an UploadedFile.

*FILES will only contain data if the request method was POST and the `<form>` that posted to the request had enctype="multipart/form-data". Otherwise, FILES will be a blank dictionary-like object.*

#### 13. HttpRequest.META

A dictionary containing all available HTTP headers. Available headers depend on the client and server, but here are some examples:

```text
CONTENT_LENGTH – The length of the request body (as a string).
CONTENT_TYPE – The MIME type of the request body.
HTTP_ACCEPT – Acceptable content types for the response.
HTTP_ACCEPT_ENCODING – Acceptable encodings for the response.
HTTP_ACCEPT_LANGUAGE – Acceptable languages for the response.
HTTP_HOST – The HTTP Host header sent by the client.
HTTP_REFERER – The referring page, if any.
HTTP_USER_AGENT – The client’s user-agent string.
QUERY_STRING – The query string, as a single (unparsed) string.
REMOTE_ADDR – The IP address of the client.
REMOTE_HOST – The hostname of the client.
REMOTE_USER – The user authenticated by the web server, if any.
REQUEST_METHOD – A string such as "GET" or "POST".
SERVER_NAME – The hostname of the server.
SERVER_PORT – The port of the server (as a string).
```

#### 14. HttpRequest.headers

A case insensitive, dict-like object that provides access to all HTTP-prefixed headers (plus Content-Length and Content-Type) from the request.

#### 15. HttpRequest.resolver_match

An instance of ResolverMatch representing the resolved URL. This attribute is only set after URL resolving took place, which means it’s available in all views but not in middleware which are executed before URL resolving takes place (you can use it in `process_view()` though).

### Attributes Set by Application Code

Django doesn’t set these attributes itself but makes use of them if set by your application.

#### 1. HttpRequest.current_app

The url template tag will use its value as the current_app argument to reverse().

#### 2. HttpRequest.urlconf

This will be used as the root URLconf for the current request, overriding the ROOT_URLCONF setting. See How Django processes a request for details.

#### 3. HttpRequest.exception_reporter_filter

This will be used instead of DEFAULT_EXCEPTION_REPORTER_FILTER for the current request. See Custom error reports for details.

#### 4. HttpRequest.exception_reporter_class

This will be used instead of DEFAULT_EXCEPTION_REPORTER for the current request. See Custom error reports for details.

### Attributes Set by Middleware

#### 1. HttpRequest.session

From the SessionMiddleware: A readable and writable, dictionary-like object that represents the current session.

#### 2. HttpRequest.site

From the CurrentSiteMiddleware: An instance of Site or RequestSite as returned by get_current_site() representing the current site.

#### 3. HttpRequest.user

From the AuthenticationMiddleware: An instance of AUTH_USER_MODEL representing the currently logged-in user. If the user isn’t currently logged in, user will be set to an instance of AnonymousUser. You can tell them apart with is_authenticated, like so:

if request.user.is_authenticated:
    ...  # Do something for logged-in users.
else:
    ...  # Do something for anonymous users.
The auser() method does the same thing but can be used from async contexts.

### Methods

#### 1. HttpRequest.auser()

From the AuthenticationMiddleware: Coroutine. Returns an instance of AUTH_USER_MODEL representing the currently logged-in user. If the user isn’t currently logged in, auser will return an instance of AnonymousUser. This is similar to the user attribute but it works in async contexts.

#### 2. HttpRequest.get_host()

Returns the originating host of the request using information from the HTTP_X_FORWARDED_HOST (if USE_X_FORWARDED_HOST is enabled) and HTTP_HOST headers, in that order. If they don’t provide a value, the method uses a combination of SERVER_NAME and SERVER_PORT as detailed in PEP 3333.

Example: "127.0.0.1:8000"

#### 3. HttpRequest.get_port()

Returns the originating port of the request using information from the HTTP_X_FORWARDED_PORT (if USE_X_FORWARDED_PORT is enabled) and SERVER_PORT META variables, in that order.

#### 4. HttpRequest.get_full_path()

Returns the path, plus an appended query string, if applicable.

```text
Example: "/music/bands/the_beatles/?print=true"
```

#### 5. HttpRequest.get_full_path_info()

Like get_full_path(), but uses path_info instead of path.

```text
Example: "/minfo/music/bands/the_beatles/?print=true"
```

#### 6. HttpRequest.build_absolute_uri(location=None)

Returns the absolute URI form of location. If no location is provided, the location will be set to request.get_full_path().

#### 7. HttpRequest.get_signed_cookie(key, default=RAISE_ERROR, salt='', max_age=None)

Returns a cookie value for a signed cookie, or raises a django.core.signing.BadSignature exception if the signature is no longer valid. If you provide the default argument the exception will be suppressed and that default value will be returned instead.

#### 8. HttpRequest.is_secure()

Returns True if the request is secure; that is, if it was made with HTTPS.

#### 9. HttpRequest.accepts(mime_type)

Returns True if the request Accept header matches the mime_type argument:

#### 10. HttpRequest.read(size=None)

#### 11. HttpRequest.readline()

#### 12. HttpRequest.readlines()

#### 13. HttpRequest.__iter__()

### Query Set Methods

QueryDict implements all the standard dictionary methods because it’s a subclass of dictionary

```python
QueryDict.__init__(query_string=None, mutable=False, encoding=None)

Instantiates a QueryDict object based on query_string.

>>> QueryDict("a=1&a=2&c=3")
<QueryDict: {'a': ['1', '2'], 'c': ['3']}>


QueryDict.__getitem__(key)

Returns the value for the given key. If the key has more than one value, it returns the last value. Raises django.utils.datastructures.MultiValueDictKeyError if the key does not exist. (This is a subclass of Python’s standard KeyError, so you can stick to catching KeyError.)


QueryDict.__setitem__(key, value)

Sets the given key to [value] (a list whose single element is value). Note that this, as other dictionary functions that have side effects, can only be called on a mutable QueryDict (such as one that was created via QueryDict.copy()).


QueryDict.__contains__(key)

Returns True if the given key is set. This lets you do, e.g., if "foo" in request.GET.


QueryDict.get(key, default=None)

Uses the same logic as *`__getitem__()`*, with a hook for returning a default value if the key doesn’t exist.


QueryDict.setdefault(key, default=None)

Like *`dict.setdefault()`*, except it uses *`__setitem__()`* internally.

QueryDict.update(other_dict)

Takes either a QueryDict or a dictionary. Like *`dict.update()`*, except it appends to the current dictionary items rather than replacing them. For example:

>>> q = QueryDict("a=1", mutable=True)
>>> q.update({"a": "2"})
>>> q.getlist("a")
['1', '2']
>>> q["a"]  # returns the last
'2'

QueryDict.items()

Like dict.items(), except this uses the same last-value logic as __getitem__() and returns an iterator object instead of a view object. For example:

>>> q = QueryDict("a=1&a=2&a=3")
>>> list(q.items())
[('a', '3')]


QueryDict.values()

Like dict.values(), except this uses the same last-value logic as __getitem__() and returns an iterator instead of a view object. For example:

>>> q = QueryDict("a=1&a=2&a=3")
>>> list(q.values())
['3']

In addition, QueryDict has the following methods:


QueryDict.copy()

Returns a copy of the object using copy.deepcopy(). This copy will be mutable even if the original was not.


QueryDict.getlist(key, default=None)

Returns a list of the data with the requested key. Returns an empty list if the key doesn’t exist and default is None. It’s guaranteed to return a list unless the default value provided isn’t a list.


QueryDict.setlist(key, list_)

Sets the given key to list_ (unlike __setitem__()).


QueryDict.appendlist(key, item)

Appends an item to the internal list associated with key.


QueryDict.setlistdefault(key, default_list=None)

Like setdefault(), except it takes a list of values instead of a single value.


QueryDict.lists()

Like items(), except it includes all values, as a list, for each member of the dictionary. For example:

>>> q = QueryDict("a=1&a=2&a=3")
>>> q.lists()
[('a', ['1', '2', '3'])]


QueryDict.pop(key)

Returns a list of values for the given key and removes them from the dictionary. Raises KeyError if the key does not exist. For example:

>>> q = QueryDict("a=1&a=2&a=3", mutable=True)
>>> q.pop("a")
['1', '2', '3']


QueryDict.popitem()

Removes an arbitrary member of the dictionary (since there’s no concept of ordering), and returns a two value tuple containing the key and a list of all values for the key. Raises KeyError when called on an empty dictionary. For example:

>>> q = QueryDict("a=1&a=2&a=3", mutable=True)
>>> q.popitem()
('a', ['1', '2', '3'])


QueryDict.dict()

Returns a dict representation of QueryDict. For every (key, list) pair in QueryDict, dict will have (key, item), where item is one element of the list, using the same logic as QueryDict.__getitem__():

>>> q = QueryDict("a=1&a=3&a=5")
>>> q.dict()
{'a': '5'}


QueryDict.urlencode(safe=None)

Returns a string of the data in query string format. For example:

>>> q = QueryDict("a=2&b=3&b=5")
>>> q.urlencode()
'a=2&b=3&b=5'

Use the safe parameter to pass characters which don’t require encoding. For example:

>>> q = QueryDict(mutable=True)
>>> q["next"] = "/a&b/"
>>> q.urlencode(safe="/")
'next=/a%26b/'
```

## Http Response Object

In contrast to HttpRequest objects, which are created automatically by Django, HttpResponse objects are your responsibility. Each view you write is responsible for instantiating, populating, and returning an HttpResponse.

### class HttpResponse

The HttpResponse class lives in the django.http module.

Typical usage is to pass the contents of the page, as a string, bytestring, or memoryview, to the HttpResponse constructor:

```python
>>> from django.http import HttpResponse
>>> response = HttpResponse("Here's the text of the web page.")
>>> response = HttpResponse("Text only, please.", content_type="text/plain")
>>> response = HttpResponse(b"Bytestrings are also accepted.")
>>> response = HttpResponse(memoryview(b"Memoryview as well."))
```

But if you want to add content incrementally, you can use response as a file-like object:

```python
>>> response = HttpResponse()
>>> response.write("<p>Here's the text of the web page.</p>")
>>> response.write("<p>Here's another paragraph.</p>")
```

#### 1. Setting header fields

To set or remove a header field in your response, use HttpResponse.headers:

```python
>>> response = HttpResponse()
>>> response.headers["Age"] = 120
>>> del response.headers["Age"]

You can also set headers on instantiation:

>>> response = HttpResponse(headers={"Age": 120})
```

### attributes

#### 1. HttpResponse.content

A bytestring representing the content, encoded from a string if necessary.

#### 2. HttpResponse.cookies

A http.cookies.SimpleCookie object holding the cookies included in the response.

#### 3. HttpResponse.headers

A case insensitive, dict-like object that provides an interface to all HTTP headers on the response, except a Set-Cookie header. See Setting header fields and HttpResponse.cookies.

#### 4. HttpResponse.charset

A string denoting the charset in which the response will be encoded. If not given at HttpResponse instantiation time, it will be extracted from content_type and if that is unsuccessful, the DEFAULT_CHARSET setting will be used.

#### 5. HttpResponse.reason_phrase

The HTTP reason phrase for the response. It uses the HTTP standard’s default reason phrases.

Unless explicitly set, reason_phrase is determined by the value of status_code.

#### 6. HttpResponse.streaming

This is always False.

This attribute exists so middleware can treat streaming responses differently from regular responses.

#### 7. HttpResponse.closed

True if the response has been closed.

### Methods

```python
HttpResponse.__init__(content=b'', content_type=None, status=200, reason=None, charset=None, headers=None)
```

Instantiates an HttpResponse object with the given page content, content type, and headers.

content is most commonly an iterator, bytestring, memoryview, or string. Other types will be converted to a bytestring by encoding their string representation. Iterators should return strings or bytestrings and those will be joined together to form the content of the response.

content_type is the MIME type optionally completed by a character set encoding and is used to fill the HTTP Content-Type header. If not specified, it is formed by 'text/html' and the DEFAULT_CHARSET settings, by default: "text/html; charset=utf-8".

status is the HTTP status code for the response. You can use Python’s http.HTTPStatus for meaningful aliases, such as HTTPStatus.NO_CONTENT.

reason is the HTTP response phrase. If not provided, a default phrase will be used.

charset is the charset in which the response will be encoded. If not given it will be extracted from content_type, and if that is unsuccessful, the DEFAULT_CHARSET setting will be used.

headers is a dict of HTTP headers for the response.

```python
HttpResponse.__setitem__(header, value)
Sets the given header name to the given value. Both header and value should be strings.

HttpResponse.__delitem__(header)
Deletes the header with the given name. Fails silently if the header doesn’t exist. Case-insensitive.

HttpResponse.__getitem__(header)
Returns the value for the given header name. Case-insensitive.

HttpResponse.get(header, alternate=None)
Returns the value for the given header, or an alternate if the header doesn’t exist.

HttpResponse.has_header(header)
Returns True or False based on a case-insensitive check for a header with the given name.

HttpResponse.items()
Acts like dict.items() for HTTP headers on the response.

HttpResponse.setdefault(header, value)
Sets a header unless it has already been set.

HttpResponse.close()
This method is called at the end of the request directly by the WSGI server.

HttpResponse.write(content)
This method makes an HttpResponse instance a file-like object.

HttpResponse.flush()
This method makes an HttpResponse instance a file-like object.

HttpResponse.tell()
This method makes an HttpResponse instance a file-like object.

HttpResponse.getvalue()
Returns the value of HttpResponse.content. This method makes an HttpResponse instance a stream-like object.

HttpResponse.readable()
Always False. This method makes an HttpResponse instance a stream-like object.

HttpResponse.seekable()
Always False. This method makes an HttpResponse instance a stream-like object.

HttpResponse.writable()
Always True. This method makes an HttpResponse instance a stream-like object.

HttpResponse.writelines(lines)
Writes a list of lines to the response. Line separators are not added. This method makes an HttpResponse instance a stream-like object.
```

Sure, let’s break down each `HttpResponse` subclass in Django, complete with examples and use cases:

## HttpsResponse subclasses

### 1. `HttpResponseRedirect`

__Description:__ This class returns a response with a 302 status code, indicating a temporary redirect. This means the client should follow the redirect URL temporarily and might need to use a different URL in the future.

__Example:__

```python
from django.http import HttpResponseRedirect

def my_view(request):
    return HttpResponseRedirect('/new-url/')
```

__Use Case:__ Use this when you need to redirect a user to another URL temporarily. For instance, after a successful form submission, you might redirect the user to a thank-you page.

### 2. `HttpResponsePermanentRedirect`

__Description:__ This class returns a response with a 301 status code, indicating a permanent redirect. This means the client should use the new URL for future requests.

__Example:__

```python
from django.http import HttpResponsePermanentRedirect

def my_view(request):
    return HttpResponsePermanentRedirect('/permanent-url/')
```

__Use Case:__ Use this when a resource has been permanently moved to a new URL. For example, if a page has been permanently moved to a new location, this status informs search engines and clients to update their bookmarks and links.

### 3. `HttpResponseNotModified`

__Description:__ This class returns a response with a 304 status code, indicating that the resource has not been modified since the last request. This response should not contain any content.

__Example:__

```python
from django.http import HttpResponseNotModified

def my_view(request):
    if not_modified_since_last_request(request):
        return HttpResponseNotModified()
    # otherwise, return the regular response
```

__Use Case:__ Use this to optimize performance by avoiding sending the same content repeatedly. For instance, in caching mechanisms, if the content hasn't changed, the server responds with 304, allowing the client to use its cached copy.

### 4. `HttpResponseBadRequest`

__Description:__ This class returns a response with a 400 status code, indicating that the server cannot process the request due to client error.

__Example:__

```python
from django.http import HttpResponseBadRequest

def my_view(request):
    if not valid_request(request):
        return HttpResponseBadRequest("Invalid request.")
    # process the request normally
```

__Use Case:__ Use this when the client sends a malformed request or invalid data. For example, if a user submits a form with missing required fields, you might return a 400 response with an error message.

### 5. `HttpResponseNotFound`

__Description:__ This class returns a response with a 404 status code, indicating that the requested resource could not be found on the server.

__Example:__

```python
from django.http import HttpResponseNotFound

def my_view(request):
    if resource_does_not_exist(request):
        return HttpResponseNotFound("Resource not found.")
    # return the resource if it exists
```

__Use Case:__ Use this when a client requests a resource that does not exist. For example, if a user navigates to a page that doesn’t exist, you’d return a 404 page.

### 6. `HttpResponseForbidden`

__Description:__ This class returns a response with a 403 status code, indicating that the client does not have permission to access the requested resource.

__Example:__

```python
from django.http import HttpResponseForbidden

def my_view(request):
    if not user_has_permission(request.user):
        return HttpResponseForbidden("You do not have permission to access this resource.")
    # process the request if permission is granted
```

__Use Case:__ Use this when a client is authenticated but does not have the necessary permissions to access a resource. For instance, a user trying to access an admin page without admin rights would receive a 403 response.

### 7. `HttpResponseNotAllowed`

__Description:__ This class returns a response with a 405 status code, indicating that the method used in the request is not allowed for the requested resource. You must provide a list of allowed methods.

__Example:__

```python
from django.http import HttpResponseNotAllowed

def my_view(request):
    if request.method not in ['GET', 'POST']:
        return HttpResponseNotAllowed(['GET', 'POST'])
    # handle allowed methods
```

__Use Case:__ Use this when a resource does not support the HTTP method used in the request. For example, if an API endpoint only supports GET and POST but a DELETE request is made, return a 405 response.

### 8. `HttpResponseGone`

__Description:__ This class returns a response with a 410 status code, indicating that the resource is no longer available and has been permanently removed.

__Example:__

```python
from django.http import HttpResponseGone

def my_view(request):
    if resource_permanently_removed(request):
        return HttpResponseGone("This resource is no longer available.")
    # process the request if the resource is available
```

__Use Case:__ Use this when a resource has been permanently deleted and will not be available again. This is useful for APIs or sites where resources have been intentionally and permanently removed.

### 9. `HttpResponseServerError`

__Description:__ This class returns a response with a 500 status code, indicating that the server encountered an internal error and was unable to complete the request.

__Example:__

```python
from django.http import HttpResponseServerError

def my_view(request):
    try:
        # code that may raise an exception
    except Exception:
        return HttpResponseServerError("An internal server error occurred.")

__Use Case:__ Use this when an unexpected server error occurs that prevents the request from being processed. For example, if a database query fails due to a server issue, you might return a 500 response.
```

Each subclass helps you convey specific types of responses, ensuring that clients receive the appropriate HTTP status code and can handle responses correctly.

## JsonResponse Objects

```python
class JsonResponse(data, encoder=DjangoJSONEncoder, safe=True, json_dumps_params=None, **kwargs)
```

An HttpResponse subclass that helps to create a JSON-encoded response. It inherits most behavior from its superclass with a couple differences:

Its default Content-Type header is set to application/json.

The first parameter, data, should be a dict instance. If the safe parameter is set to False (see below) it can be any JSON-serializable object.

The safe boolean parameter defaults to True. If it’s set to False, any object can be passed for serialization (otherwise only dict instances are allowed). If safe is True and a non-dict object is passed as the first argument, a TypeError will be raised.

```python
>>> from django.http import JsonResponse
>>> response = JsonResponse({"foo": "bar"})
>>> response.content
b'{"foo": "bar"}'
```

- Serializing non-dictionary objects
In order to serialize objects other than dict you must set the safe parameter to False:

```python
>>> response = JsonResponse([1, 2, 3], safe=False)
```

## FileResponse objects

```python
class FileResponse(open_file, as_attachment=False, filename='', **kwargs)
```

FileResponse is a subclass of StreamingHttpResponse optimized for binary files. It uses wsgi.file_wrapper if provided by the wsgi server, otherwise it streams the file out in small chunks.

If as_attachment=True, the Content-Disposition header is set to attachment, which asks the browser to offer the file to the user as a download. Otherwise, a Content-Disposition header with a value of inline (the browser default) will be set only if a filename is available.

If open_file doesn’t have a name or if the name of open_file isn’t appropriate, provide a custom file name using the filename parameter. Note that if you pass a file-like object like io.BytesIO, it’s your task to seek() it before passing it to FileResponse.

The Content-Length header is automatically set when it can be guessed from the content of open_file.

The Content-Type header is automatically set when it can be guessed from the filename, or the name of open_file.

FileResponse accepts any file-like object with binary content, for example a file open in binary mode like so:

```python
>>> from django.http import FileResponse
>>> response = FileResponse(open("myfile.png", "rb"))
```

*The file will be closed automatically, so don’t open it with a context manager.*

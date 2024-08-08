<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet"/>

# File Uploads

When Django handles a file upload, the file data ends up placed in request.FILES

```python
# Lets's Consider a FileForm
from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
```

A view handling this form will receive the file data in request.FILES, which is a dictionary containing a key for each FileField (or ImageField, or other FileField subclass) in the form. So the data from the above form would be accessible as `request.FILES['file']`.

Note that request.FILES will only contain data if the request method was POST, at least one file field was actually posted, and the `<form>` that posted the request has the attribute `enctype="multipart/form-data"`. Otherwise, request.FILES will be empty.

```python
def handle_uploaded_file(f):
    with open("some/file/name.txt", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
```

## Attributes

```python
UploadedFile.multiple_chunks(chunk_size***=None)***
Returns True if the uploaded file is big enough to require reading in multiple chunks. By default this will be any file larger than 2.5 megabytes, but that’s configurable; see below.

UploadedFile.chunks(chunk_size***=None)***
A generator returning chunks of the file. If multiple_chunks() is True, you should use this method in a loop instead of read().

In practice, it’s often easiest to use chunks() all the time. Looping over chunks() instead of using read() ensures that large files don’t overwhelm your system’s memory.

Here are some useful attributes of UploadedFile:

***UploadedFile.name***
The name of the uploaded file (e.g. my_file.txt).

***UploadedFile.size***
The size, in bytes, of the uploaded file.

***UploadedFile.content_type***
The content-type header uploaded with the file (e.g. text/plain or application/pdf). Like any data supplied by the user, you shouldn’t trust that the uploaded file is actually this type. You’ll still need to validate that the file contains the content that the content-type header claims – “trust but verify.”

***UploadedFile.content_type_extra***
A dictionary containing extra parameters passed to the content-type header. This is typically provided by services, such as Google App Engine, that intercept and handle file uploads on your behalf. As a result your handler may not receive the uploaded file content, but instead a URL or other pointer to the file (see RFC 2388).

***UploadedFile.charset***
For text/* content-types, the character set (i.e. utf8) supplied by the browser. Again, “trust but verify” is the best policy here.
```

## Csrf Exempt

```python
from django.views.decorators.csrf import csrf_exempt, csrf_protect

@csrf_exempt
def upload_file_view(request):
    request.upload_handlers.insert(0, ProgressBarUploadHandler(request))
    return _upload_file_view(request)

@csrf_protect
def_upload_file_view(request):
    # Process request
    ...
```

If you are using a class-based view, you will need to use csrf_exempt() on its dispatch() method and csrf_protect() on the method that actually processes the request. Example code:

```python
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect

@method_decorator(csrf_exempt, name="dispatch")
class UploadFileView(View):
    def setup(self, request, *args, **kwargs):
        request.upload_handlers.insert(0, ProgressBarUploadHandler(request))
        super().setup(request,*args,**kwargs)

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        # Process request
        ...
```

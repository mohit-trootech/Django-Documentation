<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet"/>

# Django Shortcut Functions

The package django.shortcuts collects helper functions and classes that “span” multiple levels of MVC. In other words, these functions/classes introduce controlled coupling for convenience’s sake.

## render

```python
render(request, template_name, context=None, content_type=None, status=None, using=None)
```

Combines a given template with a given context dictionary and returns an HttpResponse object with that rendered text.

Django does not provide a shortcut function which returns a TemplateResponse because the constructor of TemplateResponse offers the same level of convenience as render().

> Required Arguments

| request | The request object used to generate this response. |
| ------- | ---------------------------------------------------|
| template_name | The full name of a template to use or sequence of template names. If a sequence is given, the first template that exists will be used. |

> Optional Arguments

| context | A dictionary of values to add to the template context. By default, this is an empty dictionary. If a value in the dictionary is callable, the view will call it just before rendering the template. |
| ------- | ---------------------------------------------------|
| content_type | The MIME type to use for the resulting document. Defaults to 'text/html'. |
| using | The NAME of a template engine to use for loading the template. |

```python
from django.shortcuts import render

def my_view(request):
    # View code here...
    return render(
        request,
        "myapp/index.html",
        {
            "foo": "bar",
        },
        content_type="application/xhtml+xml",
    )

##This example is equivalent to:

from django.http import HttpResponse
from django.template import loader

def my_view(request):
    # View code here...
    t = loader.get_template("myapp/index.html")
    c = {"foo": "bar"}
    return HttpResponse(t.render(c, request), content_type="application/xhtml+xml")
```

## redirect()

```python
redirect(to, *args, permanent=False, **kwargs)
```

Returns an HttpResponseRedirect to the appropriate URL for the arguments passed.

The arguments could be:

- ****A model***: the model’s get_absolute_url() function will be called.*
- ****A view name, possibly with arguments***: reverse() will be used to reverse-resolve the name*
- ****An absolute or relative URL***, which will be used as-is for the redirect location.*

By default issues a temporary redirect; pass permanent=True to issue a permanent redirect.

Examples
You can use the redirect() function in a number of ways.

By passing some object; that object’s get_absolute_url() method will be called to figure out the redirect URL:

```python
from django.shortcuts import redirect

def my_view(request):
    ...
    obj = MyModel.objects.get(...)
    return redirect(obj)
```

By passing the name of a view and optionally some positional or keyword arguments; the URL will be reverse resolved using the reverse() method:

```python
def my_view(request):
    ...
    return redirect("some-view-name", foo="bar")
```

By passing a hardcoded URL to redirect to:

```python
def my_view(request):
    ...
    return redirect("/some/url/")
```

This also works with full URLs:

```python
def my_view(request):
    ...
    return redirect("<https://example.com/>")
```

By default, redirect() returns a temporary redirect. All of the above forms accept a permanent argument; if set to True a permanent redirect will be returned:

```python
def my_view(request):
    ...
    obj = MyModel.objects.get(...)
    return redirect(obj, permanent=True)
```

UseCase

```python
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

def send_message(name, message):
    # Code for actually sending the message goes here

class ContactForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

def contact_view(request):
    # The request method 'POST' indicates
    # that the form was submitted
    if request.method == 'POST':  # 1
        # Create a form instance with the submitted data
        form = ContactForm(request.POST)  # 2
        # Validate the form
        if form.is_valid():  # 3
            # If the form is valid, perform some kind of
            # operation, for example sending a message
            send_message(
                form.cleaned_data['name'],
                form.cleaned_data['message']
            )
            # After the operation was successful,
            # redirect to some other page
            return redirect('/success/')  # 4
    else:  # 5
        # Create an empty form instance
        form = ContactForm()

    return render(request, 'contact_form.html', {'form': form})
```

### Temporary vs. Permanent Redirects

The HTTP standard specifies several redirect status codes, all in the 3xx range. The two most common status codes are 301 Permanent Redirect and 302 Found.

A status code 302 Found indicates a temporary redirect. A temporary redirect says, “At the moment, the thing you’re looking for can be found at this other address.” Think of it like a store sign that reads, “Our store is currently closed for renovation. Please go to our other store around the corner.” As this is only temporary, you’d check the original address the next time you go shopping.

Note: In HTTP 1.0, the message for status code 302 was Temporary Redirect. The message was changed to Found in HTTP 1.1.

As the name implies, permanent redirects are supposed to be permanent. A permanent redirect tells the browser, “The thing you’re looking for is no longer at this address. It’s now at this new address, and it will never be at the old address again.”

A permanent redirect is like a store sign that reads, “We moved. Our new store is just around the corner.” This change is permanent, so the next time you want to go to the store, you’d go straight to the new address.

**Note: Permanent redirects can have unintended consequences. Finish this guide before using a permanent redirect or jump straight to the section “Permanent redirects are permanent.”*

```python
You could build such a response yourself from a regular HttpResponse object:

def hand_crafted_redirect_view(request):
  response = HttpResponse(status=302)
  response['Location'] = '/redirect/success/'
  return response
```

This solution is technically correct, but it involves quite a bit of typing.

Here are three examples to illustrate the different use cases:

```python
Passing a model:

from django.shortcuts import redirect

def model_redirect_view(request):
    product = Product.objects.filter(featured=True).first()
    return redirect(product)
```

`redirect()` will call `product.get_absolute_url()` and use the result as redirect target. If the given class, in this case Product, doesn’t have a `get_absolute_url()` method, this will fail with a TypeError.

```python
class Products(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField()

    def get_absolute_url(self):
        return f"/products/{self.slug}/"
```

Passing a URL name and arguments:

```python
from django.shortcuts import redirect

def fixed_featured_product_view(request):
    ...
    product_id = settings.FEATURED_PRODUCT_ID
    return redirect('product_detail', product_id=product_id)
```

`redirect()` will try to use its given arguments to reverse a URL. This example assumes your URL patterns contain a pattern like this:

```python
path('/product/<product_id>/', 'product_detail_view', name='product_detail')
```

Passing a URL:

```python
from django.shortcuts import redirect

def featured_product_view(request):
    return redirect('/products/42/')
```

`redirect()` will treat any string containing a / or . as a URL and use it as redirect target.

## get_object_or_404()

```python
get_object_or_404(klass, *args, **kwargs)
```

Calls *`get()`* on a given model manager, but it raises Http404 instead of the model’s DoesNotExist exception.

> Arguments

1. klass
A Model class, a Manager, or a QuerySet instance from which to get the object.
2. *args
Q objects.
3. **kwargs
Lookup parameters, which should be in the format accepted by get() and filter().

The following example gets the object with the primary key of 1 from MyModel:

```python
from django.shortcuts import get_object_or_404

def my_view(request):
    obj = get_object_or_404(MyModel, pk=1)

## This example is equivalent to:

from django.http import Http404

def my_view(request):
    try:
        obj = MyModel.objects.get(pk=1)
    except MyModel.DoesNotExist:
        raise Http404("No MyModel matches the given query.")
```

```python
queryset = Book.objects.filter(title__startswith="M")
get_object_or_404(queryset, pk=1)

# The above example is a bit contrived since it’s equivalent to doing:

get_object_or_404(Book, title__startswith="M", pk=1)

# but it can be useful if you are passed the queryset variable from somewhere else.

# Finally, you can also use a Manager. This is useful for example if you have a custom manager:

get_object_or_404(Book.dahl_objects, title="Matilda")
```

## get_list_or_404()

```python
get_list_or_404(klass, *args, **kwargs)
```

Returns the result of `filter()` on a given model manager cast to a list, raising Http404 if the resulting list is empty.

> Arguments

1. klass
A Model, Manager or QuerySet instance from which to get the list.
2. *args
Q objects.
3. **kwargs
Lookup parameters, which should be in the format accepted by get() and filter().

Example
The following example gets all published objects from MyModel:

```python
from django.shortcuts import get_list_or_404

def my_view(request):
    my_objects = get_list_or_404(MyModel, published=True)
```

This example is equivalent to:

```python
from django.http import Http404

def my_view(request):
    my_objects = list(MyModel.objects.filter(published=True))
    if not my_objects:
        raise Http404("No MyModel matches the given query.")
```

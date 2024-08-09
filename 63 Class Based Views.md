<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet"/>

# Class Based Views

Class-based views provide an alternative way to implement views as Python objects instead of functions. They do not replace function-based views, but have certain differences and advantages when compared to function-based views:

> Organization of code related to specific HTTP methods (GET, POST, etc.) can be addressed by separate methods instead of conditional branching.

> Object oriented techniques such as mixins (multiple inheritance) can be used to factor code into reusable components.

## Generic Views & Class Based Generic Views

In the beginning there was only the view function contract, Django passed your function an HttpRequest and expected back an HttpResponse. This was the extent of what Django provided.

> Function Based Generic views abstract common idiom and pattern & ease the process of development

The problem with function-based generic views is that while they covered the simple cases well, there was no way to extend or customize them beyond some configuration options, limiting their usefulness in many real-world applications.

Class-based generic views were created with the same objective as function-based generic views, to make view development easier. However, the way the solution is implemented, through the use of mixins, provides a toolkit that results in class-based generic views being more extensible and flexible than their function-based counterparts.

## Class Based Views

So where the code to handle HTTP GET in a view function would look something like:

```python
from django.http import HttpResponse

def my_view(request):
    if request.method == "GET":
        # <view logic>
        return HttpResponse("result")
```

In a class-based view, this would become:

from django.http import HttpResponse
from django.views import View

```python
class MyView(View):
    def get(self, request):
        # <view logic>
        return HttpResponse("result")
```

Because Django’s URL resolver expects to send the request and associated arguments to a callable function, not a class, class-based views have an *`as_view()`* class method which returns a function that can be called when a request arrives for a URL matching the associated pattern

```python
# urls.py
from django.urls import path
from myapp.views import MyView

urlpatterns = [
    path("about/", MyView.as_view()),
]
```

While a minimal class-based view does not require any class attributes to perform its job, class attributes are useful in many class-based designs, and there are two ways to configure or set class attributes.

The first is the standard Python way of subclassing and overriding attributes and methods in the subclass. So that if your parent class had an attribute greeting like this:

```python
from django.http import HttpResponse
from django.views import View

class GreetingView(View):
    greeting = "Good Day"

    def get(self, request):
        return HttpResponse(self.greeting)

# You can override that in a subclass:

class MorningGreetingView(GreetingView):
    greeting = "Morning to ya"
```

Another option is to configure class attributes as keyword arguments to the as_view() call in the URLconf:

```python
urlpatterns = [
    path("about/", GreetingView.as_view(greeting="G'day")),
]
```

## Handling a Form in Class Based Views

Let's say class based view is efficient in handling a *`form_class`*

```python
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import MyForm

def form_handling(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            # Clean & Handle Form Data
            return HttpResponseRedirect("/success/url")
    else:
        form = Myform(initial = {"key":"value"})
        return render(request, "template.html", {"form":form})
```

Som, here in function based views its very confusing with multiple if else statement, yet this is most simplest example to handle a form in function based views.

Now, lets see the same thing in class based generic views.

```python
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from .forms import MyForm

class MyFormView(View):
    form_class = MyForm
    initial = {"key": "value"}
    template_name = "form_template.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect("/success/")

        return render(request, self.template_name, {"form": form})
```

## Class Based Views Decorators

To decorate every instance of a class-based view, you need to decorate the class definition itself. To do this you apply the decorator to the *`dispatch()`* method of the class.

```python
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


class ProtectedView(TemplateView):
    template_name = "secret.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
```

Or, more succinctly, you can decorate the class instead and pass the name of the method to be decorated as the keyword argument name:

```python
@method_decorator(login_required, name="dispatch")
class ProtectedView(TemplateView):
    template_name = "secret.html"
```

If you have a set of common decorators used in several places, you can define a list or tuple of decorators and use this instead of invoking method_decorator() multiple times. These two classes are equivalent:

```python
@method_decorator(decorators, name="dispatch")
class ProtectedView(TemplateView):
    template_name = "secret.html"
```

> decorators = [never_cache, login_required]

```python
@method_decorator(never_cache, name="dispatch")
@method_decorator(login_required, name="dispatch")
class ProtectedView(TemplateView):
    template_name = "secret.html"
```

The decorators will process a request in the order they are passed to the decorator. In the example, never_cache() will process the request before login_required().

<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet"/>

# Generic Editing Views

The following views are described on this page and provide a foundation for editing content:

```python
django.views.generic.edit.FormView
django.views.generic.edit.CreateView
django.views.generic.edit.UpdateView
django.views.generic.edit.DeleteView
```

Example Model: myapp/models.py:

```python
from django.db import models
from django.urls import reverse

class Author(models.Model):
    name = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse("author-detail", kwargs={"pk": self.pk})
```

## FormView Class

```python
django.views.generic.edit.FormView
```

A view that displays a form. On error, redisplays the form with validation errors; on success, redirects to a new URL.

Ancestors (MRO)

This view inherits methods and attributes from the following views:

```python
django.views.generic.base.TemplateResponseMixin
django.views.generic.edit.BaseFormView
django.views.generic.edit.FormMixin
django.views.generic.edit.ProcessFormView
django.views.generic.base.View
```

Example myapp/forms.py:

```python
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass
```

Example myapp/views.py:

```python
from myapp.forms import ContactForm
from django.views.generic.edit import FormView

class ContactFormView(FormView):
    template_name = "contact.html"
    form_class = ContactForm
    success_url = "/thanks/"

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)
```

Example myapp/contact.html:

```html
<form method="post">{% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Submit">
</form>
```

<form method="post" class="mx-auto m-3">
<label for="name" class="form-label">Email Address:
<input type='text' class="form-control" placeholder="Enter Your Email Address" id="name" name="name">
<br>
<label for="textarea" class="form-label">Email Body:
<textarea class="form-control" id="textarea" name="textarea" placeholder="Enter Your Message"></textarea>
<br>
<button type="submit" value="Send message" role="button" class="btn btn-primary">Hello</button>
</form>

```python
class django.views.generic.edit.BaseFormView
```

A base view for displaying a form. It is not intended to be used directly, but rather as a parent class of the django.views.generic.edit.FormView or other views displaying a form.

Ancestors (MRO)

This view inherits methods and attributes from the following views:

```python
django.views.generic.edit.FormMixin
django.views.generic.edit.ProcessFormView
```

## CreateView Class

```python
class django.views.generic.edit.CreateView
```

A view that displays a form for creating an object, redisplaying the form with validation errors (if there are any) and saving the object.

Ancestors (MRO)

This view inherits methods and attributes from the following views:

```python
django.views.generic.detail.SingleObjectTemplateResponseMixin
django.views.generic.base.TemplateResponseMixin
django.views.generic.edit.BaseCreateView
django.views.generic.edit.ModelFormMixin
django.views.generic.edit.FormMixin
django.views.generic.detail.SingleObjectMixin
django.views.generic.edit.ProcessFormView
django.views.generic.base.View
```

### Attributes

> ***template_name_suffix***
The CreateView page displayed to a GET request uses a template_name_suffix of '_form'. For example, changing this attribute to '_create_form' for a view creating objects for the example Author model would cause the default template_name to be 'myapp/author_create_form.html'.

> ***object***
When using CreateView you have access to self.object, which is the object being created. If the object hasn’t been created yet, the value will be None.

```python
from django.views.generic.edit import CreateView
from myapp.models import Author

class AuthorCreateView(CreateView):
    model = Author
    fields = ["name"]
```

Example myapp/author_form.html:

```html
<form method="post">{% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Save">
</form>
```

```python
class django.views.generic.edit.BaseCreateView
```

A base view for creating a new object instance. It is not intended to be used directly, but rather as a parent class of the django.views.generic.edit.CreateView.

Ancestors (MRO)

This view inherits methods and attributes from the following views:

```pythpn
django.views.generic.edit.ModelFormMixin
django.views.generic.edit.ProcessFormView
```

Methods

```python
get(request, *args, **kwargs)
Sets the current object instance (self.object) to None.

post(request, *args, **kwargs)
Sets the current object instance (self.object) to None.
```

## UpdateView Class

```python
class django.views.generic.edit.UpdateView
```

A view that displays a form for editing an existing object, redisplaying the form with validation errors (if there are any) and saving changes to the object. This uses a form automatically generated from the object’s model class (unless a form class is manually specified).

Ancestors (MRO)

This view inherits methods and attributes from the following views:

```python
django.views.generic.detail.SingleObjectTemplateResponseMixin
django.views.generic.base.TemplateResponseMixin
django.views.generic.edit.BaseUpdateView
django.views.generic.edit.ModelFormMixin
django.views.generic.edit.FormMixin
django.views.generic.detail.SingleObjectMixin
django.views.generic.edit.ProcessFormView
django.views.generic.base.View
```

Attributes

> ***-> template_name_suffix***
The UpdateView page displayed to a GET request uses a template_name_suffix of '_form'. For example, changing this attribute to '_update_form' for a view updating objects for the example Author model would cause the default template_name to be 'myapp/author_update_form.html'.

> ***->object***
When using UpdateView you have access to self.object, which is the object being updated.

Example myapp/views.py:

```python
from django.views.generic.edit import UpdateView
from myapp.models import Author

class AuthorUpdateView(UpdateView):
    model = Author
    fields = ["name"]
    template_name_suffix = "_update_form"
    success_url = "?"
```

Example myapp/author_update_form.html:

```html
<form method="post">{% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Update">
</form>
```

```python
class django.views.generic.edit.BaseUpdateView
```

A base view for updating an existing object instance. It is not intended to be used directly, but rather as a parent class of the django.views.generic.edit.UpdateView.

Ancestors (MRO)

This view inherits methods and attributes from the following views:

```python
django.views.generic.edit.ModelFormMixin
django.views.generic.edit.ProcessFormView
```

Methods

```python
get(request, *args, **kwargs)

# Sets the current object instance (self.object).

post(request, *args, **kwargs)
Sets the current object instance (self.object).
```

## DeleteView Class

```python
class django.views.generic.edit.DeleteView
```

A view that displays a confirmation page and deletes an existing object. The given object will only be deleted if the request method is POST. If this view is fetched via GET, it will display a confirmation page that should contain a form that POSTs to the same URL.

Ancestors (MRO)

This view inherits methods and attributes from the following views:

```python
django.views.generic.detail.SingleObjectTemplateResponseMixin
django.views.generic.base.TemplateResponseMixin
django.views.generic.edit.BaseDeleteView
django.views.generic.edit.DeletionMixin
django.views.generic.edit.FormMixin
django.views.generic.base.ContextMixin
django.views.generic.detail.BaseDetailView
django.views.generic.detail.SingleObjectMixin
django.views.generic.base.View
```

Attributes

> ***-> form_class***
Inherited from BaseDeleteView. The form class that will be used to confirm the request. By default django.forms.Form, resulting in an empty form that is always valid.

By providing your own Form subclass, you can add additional requirements, such as a confirmation checkbox, for example.

> ***-> template_name_suffix***
The DeleteView page displayed to a GET request uses a template_name_suffix of '_confirm_delete'. For example, changing this attribute to '_check_delete' for a view deleting objects for the example Author model would cause the default template_name to be 'myapp/author_check_delete.html'.

Example myapp/views.py:

```python
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from myapp.models import Author

class AuthorDeleteView(DeleteView):
    model = Author
    success_url = reverse_lazy("author-list")
```

Example myapp/author_confirm_delete.html:

```html
<form method="post">{% csrf_token %}
    <p>Are you sure you want to delete "{{ object }}"?</p>
    {{ form }}
    <input type="submit" value="Confirm">
</form>
```

```python
class django.views.generic.edit.BaseDeleteView
```

A base view for deleting an object instance. It is not intended to be used directly, but rather as a parent class of the django.views.generic.edit.DeleteView.

Ancestors (MRO)

This view inherits methods and attributes from the following views:

```python
django.views.generic.edit.DeletionMixin
django.views.generic.edit.FormMixin
django.views.generic.detail.BaseDetailView
```

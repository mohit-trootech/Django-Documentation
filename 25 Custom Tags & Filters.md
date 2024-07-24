<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet" />

# How to create custom template tags and filters

## Code layout

The most common place to specify custom template tags and filters is inside a Django app. If they relate to an existing app, it makes sense to bundle them there; otherwise, they can be added to a new app. When a Django app is added to INSTALLED_APPS, any tags it defines in the conventional location described below are automatically made available to load within templates.

Here you will se the directory of polls application :-

```bash
.
├── admin.py
├── apps.py
├── __init__.py
├── migrations
│   ├── 0001_initial.py
│   ├── __init__.py
├── models.py
├── templatetags
│   ├── __init__.py
│   └── shuffle.py
├── tests.py
├── urls.py
└── views.py
```

And in your template you would use the following:

    {% load shuffle %}

To be a valid tag library, the module must contain a module-level variable named register that is a template.Library instance, in which all the tags and filters are registered. So, near the top of your module, put the following:

    from django import template

    register = template.Library()

<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet"/>

# Context Processors

A context processor is a function that takes the current HttpRequest object as an argument and returns a dictionary of variables that can be made available to all templates. These variables are added to the context of the request, meaning that they can be accessed in any template that is rendered as a result of that request. This allows you to include common information, such as a site logo or user details, on every page of your website, without having to include the same code in multiple views.

## Create Custom Context Processor

Here's an example of how you could use a context processor to add a site logo and footer information to all pages

- Create a folder called `utils` in your project.
- Inside the utils folder, create a file called `context_processors.py`.
- In the context_processors.py, import the models you need, and define two context processor functions: one to handle the site logo, and one to handle the footer information.

```python
# context_processors.py

from myapp.models import SiteLogo, FooterInfo

def logo_context(request):
    logo = SiteLogo.objects.first()
    return {'logo': logo}

def footer_context(request):
    footer_info = FooterInfo.objects.first()
    return {'footer_info': footer_info}
```

## Add Context Processor into Setting

```python
TEMPLATES = [
    {
        ...
        'OPTIONS': {
            'context_processors': [
                ...
                'utils.context_processors.logo_context',
                'utils.context_processors.footer_context',
            ],
        },
    },
]
```

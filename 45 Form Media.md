<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet" />

# Form Media

Rendering an attractive and easy-to-use web form requires more than just HTML - it also requires CSS stylesheets, and if you want to use fancy widgets, you may also need to include some JavaScript on each page. The exact combination of CSS and JavaScript that is required for any given page will depend upon the widgets that are in use on that page.

## Assets as Static Medium

The easiest way to define assets is as a static definition. Using this method, the declaration is an inner Media class. The properties of the inner class define the requirements.

```python
from django import forms


class CalendarWidget(forms.TextInput):
    class Media:
        css = {
            "all": ["pretty.css"],
        }
        js = ["animations.js", "actions.js"]
```

This code defines a CalendarWidget, which will be based on TextInput. Every time the CalendarWidget is used on a form, that form will be directed to include the CSS file pretty.css, and the JavaScript files animations.js and actions.js.

```bash
>>> w = CalendarWidget()
>>> print(w.media)
<link href="http://static.example.com/pretty.css" media="all" rel="stylesheet">
<script src="http://static.example.com/animations.js"></script>
<script src="http://static.example.com/actions.js"></script>
```

# CSS

A dictionary describing the CSS files required for various forms of output media.

The values in the dictionary should be a tuple/list of file names. See the section on paths for details of how to specify paths to these files.

The keys in the dictionary are the output media types. These are the same types accepted by CSS files in media declarations: ‘all’, ‘aural’, ‘braille’, ‘embossed’, ‘handheld’, ‘print’, ‘projection’, ‘screen’, ‘tty’ and ‘tv’. If you need to have different stylesheets for different media types, provide a list of CSS files for each output medium. The following example would provide two CSS options – one for the screen, and one for print:

```python
class Media:
    css = {
        "screen": ["pretty.css"],
        "print": ["newspaper.css"],
        "tv,projector": ["lo_res.css"],
    }
```

# JavaScript

A tuple describing the required JavaScript files. See the section on paths for details of how to specify paths to these files.

By default, any object using a static Media definition will inherit all the assets associated with the parent widget. This occurs regardless of how the parent defines its own requirements. For example, if we were to extend our basic Calendar widget from the example above:

```python
>>> class FancyCalendarWidget(CalendarWidget):
...     class Media:
...         css = {
...             "all": ["fancy.css"],
...         }
...         js = ["whizbang.js"]
...
```

```bash
>>> w = FancyCalendarWidget()
>>> print(w.media)
<link href="http://static.example.com/pretty.css" media="all" rel="stylesheet">
<link href="http://static.example.com/fancy.css" media="all" rel="stylesheet">
<script src="http://static.example.com/animations.js"></script>
<script src="http://static.example.com/actions.js"></script>
<script src="http://static.example.com/whizbang.js"></script>
```

The FancyCalendar widget inherits all the assets from its parent widget. If you don’t want Media to be inherited in this way, add an extend=False declaration to the Media declaration:

```python
>>> class FancyCalendarWidget(CalendarWidget):
...     class Media:
...         extend = False
...         css = {
...             "all": ["fancy.css"],
...         }
...         js = ["whizbang.js"]
...

>>> w = FancyCalendarWidget()
>>> print(w.media)
<link href="http://static.example.com/fancy.css" media="all" rel="stylesheet">
<script src="http://static.example.com/whizbang.js"></script>
```

If you require even more control over inheritance, define your assets using a dynamic property. Dynamic properties give you complete control over which files are inherited, and which are not.

### Paths as String

String paths used to specify assets can be either relative or absolute. If a path starts with /, http:// or https://, it will be interpreted as an absolute path, and left as-is. All other paths will be prepended with the value of the appropriate prefix. If the django.contrib.staticfiles app is installed, it will be used to serve assets.

```python
>>> from django import forms
>>> class CalendarWidget(forms.TextInput):
...     class Media:
...         css = {
...             "all": ["/css/pretty.css"],
...         }
...         js = ["animations.js", "http://othersite.com/actions.js"]
...

>>> w = CalendarWidget()
>>> print(w.media)
<link href="/css/pretty.css" media="all" rel="stylesheet">
<script src="http://uploads.example.com/animations.js"></script>
<script src="http://othersite.com/actions.js"></script>
```

### Paths as Object

Asset paths may also be given as hashable objects implementing an `__html__()` method. The `__html__()` method is typically added using the html_safe() decorator.

```python
>>> from django import forms
>>> from django.utils.html import html_safe
>>>
>>> @html_safe
... class JSPath:
...     def __str__(self):
...         return '<script src="https://example.org/asset.js" defer>'
...

>>> class SomeWidget(forms.TextInput):
...     class Media:
...         js = [JSPath()]
...
```

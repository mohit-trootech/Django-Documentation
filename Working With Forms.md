<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet" />

# Django Forms

Unless you’re planning to build websites and applications that do nothing but publish content, and don’t accept input from your visitors, you don't not need to understand and use forms.

Django provides a range of tools and libraries to help you build forms to accept input from site visitors, and then process and respond to the input.

## HTML Forms

In HTML, a form is a collection of elements inside `<form>...</form>` that allow a visitor to do things like enter text, select options, manipulate objects or controls, and so on, and then send that information back to the server.

Some of these form interface elements - text input or checkboxes - are built into HTML itself. Others are much more complex; an interface that pops up a date picker or allows you to move a slider or manipulate controls will typically use JavaScript and CSS as well as HTML form `<input>` elements to achieve these effects.

A form must specify two things:

1. ***where***: the URL to which the data corresponding to the user’s input should be returned
2. ***how***: the HTTP method the data should be returned by

As an example, the login form for the Django admin contains several `<input>` elements: one of type="text" for the username, one of type="password" for the password, and one of type="submit" for the “Log in” button. It also contains some hidden text fields that the user doesn’t see, which Django uses to determine what to do next.

## GET and POST

GET and POST are the only HTTP methods to use when dealing with forms.

Django’s login form is returned using the POST method, in which the browser bundles up the form data, encodes it for transmission, sends it to the server, and then receives back its response.

GET, by contrast, bundles the submitted data into a string, and uses this to compose a URL. The URL contains the address where the data must be sent, as well as the data keys and values. You can see this in action if you do a search in the Django documentation, which will produce a URL of the form

    <https://docs.djangoproject.com/search/?q=forms&release=1>.

GET and POST are typically used for different purposes.

Any request that could be used to change the state of the system - for example, a request that makes changes in the database - should use POST. GET should be used only for requests that do not affect the state of the system.

GET would also be unsuitable for a password form, because the password would appear in the URL, and thus, also in browser history and server logs, all in plain text. Neither would it be suitable for large quantities of data, or for binary data, such as an image. A web application that uses GET requests for admin forms is a security risk: it can be easy for an attacker to mimic a form’s request to gain access to sensitive parts of the system. POST, coupled with other protections like Django’s CSRF protection offers more control over access.

On the other hand, GET is suitable for things like a web search form, because the URLs that represent a GET request can easily be bookmarked, shared, or resubmitted.

## Django role in Forms

Handling forms is a complex business. Consider Django’s admin, where numerous items of data of several different types may need to be prepared for display in a form, rendered as HTML, edited using a convenient interface, returned to the server, validated and cleaned up, and then saved or passed on for further processing.

Django’s form functionality can simplify and automate vast portions of this work, and can also do it more securely than most programmers would be able to do in code they wrote themselves.

Django handles three distinct parts of the work involved in forms:

- preparing and restructuring data to make it ready for rendering
- creating HTML forms for the data
- receiving and processing submitted forms and data from the client
It is possible to write code that does all of this manually, but Django can take care of it all for you.

## Forms in Django

In the context of a web application, ‘form’ might refer to that HTML `<form>`, or to the Django Form that produces it, or to the structured data returned when it is submitted, or to the end-to-end working collection of these parts.

### Django Form Class

In much the same way that a Django model describes the logical structure of an object, its behavior, and the way its parts are represented to us, a Form class describes a form and determines how it works and appears.

In a similar way that a model class’s fields map to database fields, a form class’s fields map to HTML form `<input>` elements. (A ModelForm maps a model class’s fields to HTML form `<input>` elements via a Form; this is what the Django admin is based upon.)

A form’s fields are themselves classes; they manage form data and perform validation when a form is submitted. A DateField and a FileField handle very different kinds of data and have to do different things with it.

A form field is represented to a user in the browser as an HTML “widget” - a piece of user interface machinery. Each field type has an appropriate default Widget class, but these can be overridden as required.

## Build a Form

Suppose you want to create a simple form on your website, Polls.

So, we are working on poll application and now we are require to add form that takes question and choices from user

### Forms Template: The Form Class

Now, Lets add a forms.py File in Polls application.

A Simple Form Can be Created using Form Class Template

    from django import forms

    class NameForm(forms.Form):
        your_name = forms.CharField(label="Your name", max_length=100)

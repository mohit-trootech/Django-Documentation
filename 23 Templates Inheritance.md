<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/
bootstrap.min.css" rel="stylesheet" />

# Templates Inheritance

The most powerful – and thus the most complex – part of Django’s template engine is template inheritance. Template inheritance allows you to build a base “skeleton” template that contains all the common elements of your site and defines blocks that child templates can override.

Now, as Python offer DRY (don't Repeat Yourself), So Django Provide Some Template Inheritance Feature allow us to inherit templates multiple times, Components Like Navbar, Footer, boiler Plate & Some Components are Just Static and don't require to rewrite again.

Template Inheritance allow to inherit the template to use the same content multiple times in different templates, Lets Understand this with a Examples,

***Directory***

```bash
.
├── index.html
├── polls
│   ├── details.html
│   ├── home.html
│   └── results.html
└── static
    ├── images
    │   └── polls.png
    ├── scripts.js
    └── style.css
```

So Here My `index.html` works as a Template for all the polls htmls, Since the Navbar is Always Same, I just need to Update the Content block.

    {% load static %}
    <!doctype html>
    <html lang="en">

    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        {% block title %}<title>Bootstrap demo</title>{% endblock %}
        <link rel="stylesheet" href="{% static 'style.css' %}">
        <link rel="shortcut icon" href="{% static 'images/polls.png' %}" type="image/x-icon">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css"
            integrity="sha512-Kc323vGBEqzTmouAECnVceyQqyqdsSiqLQISBL29aUW4U/M7pSPA/gEUZQqv1cwx4OnYxTxve5UMg5GT6L4JJg=="
            crossorigin="anonymous" referrerpolicy="no-referrer" />
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet"
            integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    </head>

    <body data-bs-theme="dark">
        <!-- Navbar -->
        <nav class="navbar navbar-expand-lg bg-body-tertiary">
            <a href="/polls" class="container-fluid text-decoration-none">
                <span class="navbar-brand mb-0 h1">Polls Application Django</span>
            </a>
            <!-- Theme Toggle Start -->
            <div class="theme-toggle mx-3">
                <label class="switch">
                    <input type="checkbox" name="theme" id="theme" checked />
                    <span class="slider"></span>
                </label>
            </div>
            <!-- Theme Toggle End -->
        </nav>

        <!-- Content -->
        <div class="container my-3">
            {% block content %} {% endblock %}
        </div>

    </body>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js"
        integrity="sha384-I7E8VVD/ismYTF4hNIPjVp/Zjvgyol6VFvRkX/vR+Vc4jQkC+hVqc2pM8ODewa9r"
        crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.min.js"
        integrity="sha384-0pUGZvbkm6XF6gxjEnlmuGrJXVbNuzT9qBBavbLwCsOGabYfZo0T0to5eqruptLy"
        crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.slim.min.js"
        integrity="sha512-sNylduh9fqpYUK5OYXWcBleGzbZInWj8yCJAU57r1dpSK9tP2ghf/SRYCMj+KsslFkCOt3TvJrX2AV/Gc3wOqA=="
        crossorigin="anonymous" referrerpolicy="no-referrer"></script>
    <script src="{% static 'scripts.js' %}"></script>
    {% block script-js %}{% endblock %}

    </html>

So, Here is index.html file and as you see it contains all the tags required to load HTML i.e. `html`, `head`, `body`

But The Title & Content need to Change Each Time we Change HTML so use block statement.

In this example, the `block` tag defines three blocks that child templates can fill in. All the `block` tag does is to tell the template engine that a child template may override those portions of the template.

Lets See `polls/details.html`

    `{% extends 'index.html' %}
    {% load static %}
    {% load shuffle %}
    {% block title %}Details{% endblock %}
    {% block content %}
    <form class="card mb-3" action="{% url 'vote' question.id %}" method="post">
        {% csrf_token %}
        <div class="card-body">
            <h5 class="card-title">{{question}}</h5>
            <ul class="list-group list-group-flush">
                {% for choice in question.choice_set.all|shuffle %}
                <li class="list-group-item">
                    <input class="form-check-input me-1" type="radio" name="questionChoice" id="firstRadio"
                        value="{{choice.id}}">
                    <label class="form-check-label" for="firstRadio">{{choice.choice_text}}</label>
                </li>
                {% endfor %}
            </ul>
        </div>
        <button type="submit" class="btn btn-primary m-3">Submit</button>
    </form>
    {% if error_message %}
    <div class="toast-container position-fixed bottom-0 end-0 p-3" id="toastContainer">
        <div id="liveToast" class="toast fade show" role="alert" aria-live="assertive" aria-atomic="true"
            data-autohide="true">
            <div class="toast-header">
                <img src="{% static 'images/polls.png' %}" class="rounded me-2" alt="polls_error" width="32" height="32">
                <strong class="me-auto">Polls Error</strong>
                <small>Recently</small>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                {{error_message}}
            </div>
        </div>
    </div>
    {% endif %}
    {% endblock %}
    {% block script-js %}
    <script>
        document.addEventListener("DOMContentLoaded", () => {
            const toast = document.getElementById("toastContainer");
            setTimeout(() => {
                if (toast) {
                    toast.style.display = "none";
                };
            }, 3000);
        });
    </script>
    {% endblock %}`

Here we `extends` index.html and use block to update or override the content of index.html, ***Similarly for `polls/home.html`, `polls/results.html`***

### home.html

    {% extends 'index.html' %}
    {% block content %}
    <div class="list-group">
        {% if questions %}
        {% for question in questions %}
        <a type="button" href="{% url 'details' question.id %}" class="list-group-item list-group-item-action">
            <i class="fa fa-arrow-up-right-from-square"></i><span> {{question.question_text}}</span></>
            {% endfor %}
            {% else %}
            <button type="button" class="list-group-item list-group-item-action">
                NO QUESTIONS AVAILABLE
            </button>
            {% endif %}
    </div>
    {% endblock %}

### Results.html

    {% extends 'index.html' %}
    {% block title %}Result{% endblock %}
    {% block content %}
    <table class="table table-hover">
        <thead>
            <tr>
                <th scope="col">#</th>
                <th scope="col">Choices</th>
                <th scope="col">Result</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <th colspan="3" class="text-center fs-3">{{question.question_text}}</th>
            </tr>
            {% for choice in question.choice_set.all %}
            <tr>
                <th>{{forloop.counter}}</th>
                <td>{{choice.choice_text}}</td>
                <td>{{choice.votes}} Votes</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    <a type="button" href="/polls" class="btn btn-primary">Go Back To Home</a>
    <a type="button" href="{% url 'details' question.id %}" class="btn btn-primary">Poll Again For Same Question</a>
    {% endblock %}

## include.html

The include tag allows you to include a template inside the current template.

This is useful when you have a block of content that is the same for many pages.

So we Have Navbar in HTML, Now What if we Create a NavBar HTML Sperate and include it in our index.html

    {% block navbar %}
    <!-- Navbar Start -->
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <a href="/polls" class="container-fluid text-decoration-none">
            <span class="navbar-brand mb-0 h1">Polls Application Django</span>
        </a>
        <!-- Theme Toggle Start -->
        <div class="theme-toggle mx-3">
            <label class="switch">
                <input type="checkbox" name="theme" id="theme" checked />
                <span class="slider"></span>
            </label>
        </div>
        <!-- Theme Toggle End -->
    </nav>
    <!-- Navbar End -->
    {% endblock %}

Updates `index.html`,

    {% load static %}
    <!doctype html>
    <html lang="en">

    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        {% block title %}<title>Bootstrap demo</title>{% endblock %}
        <link rel="stylesheet" href="{% static 'style.css' %}">
        <link rel="shortcut icon" href="{% static 'images/polls.png' %}" type="image/x-icon">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css"
            integrity="sha512-Kc323vGBEqzTmouAECnVceyQqyqdsSiqLQISBL29aUW4U/M7pSPA/gEUZQqv1cwx4OnYxTxve5UMg5GT6L4JJg=="
            crossorigin="anonymous" referrerpolicy="no-referrer" />
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet"
            integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    </head>

    <body data-bs-theme="dark">
        {% includes 'navbar.html' %}
        {% block navbar %}{% endblock %}
        <!-- Content -->
        <div class="container my-3">
            {% block content %} {% endblock %}
        </div>
    </body>
    </html>

Same Template Different Approach

## Benifits of Django Template Inheritance

1. **Modularity**: Template extends promote modularity by allowing you to separate common elements from specific content. This makes your codebase cleaner, more maintainable, and easier to understand.

2. **Code Reusability**: With template extends, you can create a base template containing shared components, such as a navigation bar or footer. These components can be reused across multiple pages, saving you time and effort.

3. **Consistency**: By using a base template, you ensure consistency across different pages of your website. All child templates automatically reflect any changes made to the base template.

4. **Easy Updates**: When you need to make changes to a shared component, you only have to modify the base template. The changes will be reflected in all child templates that extend it, eliminating the need for manual updates in multiple places.

<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet" />

# Views

A view is a “type” of web page in your Django application that generally serves a specific function and has a specific template. For example, in a blog application, you might have the following views:

### Blog homepage – displays the latest few entries

### Entry “detail” page – permalink page for a single entry

### Year-based archive page – displays all months with entries in the given year

### Month-based archive page – displays all days with entries in the given month

### Day-based archive page – displays all entries in the given day

### Comment action – handles posting comments to a given entry

In our poll application, we’ll have the following four views:

### Question “index” page – displays the latest few questions

### Question “detail” page – displays a question text, with no results but with a form to vote

### Question “results” page – displays results for a particular question

### Vote action – handles voting for a particular choice in a particular question

In Django, web pages and other content are delivered by views. Each view is represented by a Python function (or method, in the case of class-based views). Django will choose a view by examining the URL that’s requested (to be precise, the part of the URL after the domain name).

## Writing Some Views

Now let’s add a few more views to polls/views.py. These views are slightly different, because they take an argument:

    def detail(request, question_id):
        return HttpResponse("You're looking at question %s." % question_id)

    def results(request, question_id):
        response = "You're looking at the results of question %s."
        return HttpResponse(response % question_id)

    def vote(request, question_id):
        return HttpResponse("You're voting on question %s." % question_id)

With These New Views, Lets map some urls,

    from django.urls import path

    from . import views

    urlpatterns = [
        # ex: /polls/
        path("", views.index, name="index"),
        # ex: /polls/5/
        path("<int:question_id>/", views.detail, name="detail"),
        # ex: /polls/5/results/
        path("<int:question_id>/results/", views.results, name="results"),
        # ex: /polls/5/vote/
        path("<int:question_id>/vote/", views.vote, name="vote"),
    ]

Now We need to include These with the main URLs Configuration.

1. Open `mysite.urls` file and include the url of `polls.urls`

        from django.contrib import admin
        from django.urls import include, path

        urlpatterns = [
            path("polls/", include("polls.urls")),
            path("admin/", admin.site.urls),
        ]

The include method is used to include the apps urls with main urls config

### Now when we follow the urls, then we will see the views function Content, Lets understand this with some examples

1. `localhost/polls` - Here you will see home page

2. `localhost/polls/5` - Here you will see - `You're looking at question 5.`

3. `localhost/polls/5/vote` - Here you will see - `You're voting on question 5`

4. `localhost/polls/5/result` - Here you will see - `You're looking at the results of question 5.`

***Lets Understand the some working views with some functionality in next module***

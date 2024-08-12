<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet"/>

# Generic Date Views

Date-based generic views, provided in django.views.generic.dates, are views for displaying drilldown pages for date-based data.

Sample Model

```python
from django.db import models
from django.urls import reverse


class Article(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateField()

    def get_absolute_url(self):
        return reverse("article-detail", kwargs={"pk": self.pk})
```

## 1. ArchiveIndexView

```python
class ArchiveIndexView
```

A top-level index page showing the “latest” objects, by date. Objects with a date in the future are not included unless you set allow_future to True.

Ancestors (MRO)

```python
django.views.generic.list.MultipleObjectTemplateResponseMixin
django.views.generic.base.TemplateResponseMixin
django.views.generic.dates.BaseArchiveIndexView
django.views.generic.dates.BaseDateListView
django.views.generic.list.MultipleObjectMixin
django.views.generic.dates.DateMixin
django.views.generic.base.View
```

Context

In addition to the context provided by *`django.views.generic.list.MultipleObjectMixin (via django.views.generic.dates.BaseDateListView)`*, the template’s context will be:

***date_list***: A QuerySet object containing all years that have objects available according to queryset, represented as datetime.datetime objects, in descending order.
Notes

> Uses a default context_object_name of latest.
Uses a default template_name_suffix of _archive.

Defaults to providing date_list by year, but this can be altered to month or day using the attribute date_list_period. This also applies to all subclass views.
Example myapp/urls.py:

```python
from django.urls import path
from django.views.generic.dates import ArchiveIndexView

from myapp.models import Article

urlpatterns = [
    path(
        "archive/",
        ArchiveIndexView.as_view(model=Article, date_field="pub_date"),
        name="article_archive",
    ),
]
```

Example myapp/article_archive.html:

```html
<ul>
    {% for article in latest %}
        <li>{{ article.pub_date }}: {{ article.title }}</li>
    {% endfor %}
</ul>
This will output all articles.
```

## 2. YearArchiveView

```python
class YearArchiveView
```

A yearly archive page showing all available months in a given year. Objects with a date in the future are not displayed unless you set *`allow_future`* to *`True`*.

Ancestors (MRO)

```python
django.views.generic.list.MultipleObjectTemplateResponseMixin
django.views.generic.base.TemplateResponseMixin
django.views.generic.dates.BaseYearArchiveView
django.views.generic.dates.YearMixin
django.views.generic.dates.BaseDateListView
django.views.generic.list.MultipleObjectMixin
django.views.generic.dates.DateMixin
django.views.generic.base.View
```

```text
make_object_list
A boolean specifying whether to retrieve the full list of objects for this year and pass those to the template. If True, the list of objects will be made available to the context. If False, the None queryset will be used as the object list. By default, this is False.

get_make_object_list()
Determine if an object list will be returned as part of the context. Returns make_object_list by default.
```

Context

In addition to the context provided by django.views.generic.list.MultipleObjectMixin (via django.views.generic.dates.BaseDateListView), the template’s context will be:

```text
date_list: A QuerySet object containing all months that have objects available according to queryset, represented as datetime.datetime objects, in ascending order.

year: A date object representing the given year.
next_year: A date object representing the first day of the next year, according to allow_empty and allow_future.

previous_year: A date object representing the first day of the previous year, according to allow_empty and allow_future.
Notes
```

Uses a default template_name_suffix of _archive_year.
Example myapp/views.py:

```python
from django.views.generic.dates import YearArchiveView

from myapp.models import Article

class ArticleYearArchiveView(YearArchiveView):
    queryset = Article.objects.all()
    date_field = "pub_date"
    make_object_list = True
    allow_future = True
```

Example myapp/urls.py:

```python
from django.urls import path

from myapp.views import ArticleYearArchiveView

urlpatterns = [
    path("<int:year>/", ArticleYearArchiveView.as_view(), name="article_year_archive"),
]
```

Example myapp/article_archive_year.html:

```html
<ul>
    {% for date in date_list %}
        <li>{{ date|date }}</li>
    {% endfor %}
</ul>

<div>
    <h1>All Articles for {{ year|date:"Y" }}</h1>
    {% for obj in object_list %}
        <p>
            {{ obj.title }} - {{ obj.pub_date|date:"F j, Y" }}
        </p>
    {% endfor %}
</div>
```

## 3. MonthArchiveView

```python
class MonthArchiveView
```

A monthly archive page showing all objects in a given month. Objects with a date in the future are not displayed unless you set allow_future to True.

Ancestors (MRO)

```python
django.views.generic.list.MultipleObjectTemplateResponseMixin
django.views.generic.base.TemplateResponseMixin
django.views.generic.dates.BaseMonthArchiveView
django.views.generic.dates.YearMixin
django.views.generic.dates.MonthMixin
django.views.generic.dates.BaseDateListView
django.views.generic.list.MultipleObjectMixin
django.views.generic.dates.DateMixin
django.views.generic.base.View
```

Context

In addition to the context provided by MultipleObjectMixin (via BaseDateListView), the template’s context will be:

```text
date_list: A QuerySet object containing all days that have objects available in the given month, according to queryset, represented as datetime.datetime objects, in ascending order.

month: A date object representing the given month.
next_month: A date object representing the first day of the next month, according to allow_empty and allow_future.

previous_month: A date object representing the first day of the previous month, according to allow_empty and allow_future.
```

Notes

Uses a default template_name_suffix of _archive_month.
Example myapp/views.py:

```python
from django.views.generic.dates import MonthArchiveView

from myapp.models import Article

class ArticleMonthArchiveView(MonthArchiveView):
    queryset = Article.objects.all()
    date_field = "pub_date"
    allow_future = True
Example myapp/urls.py:

from django.urls import path

from myapp.views import ArticleMonthArchiveView

urlpatterns = [
    # Example: /2012/08/
    path(
        "<int:year>/<int:month>/",
        ArticleMonthArchiveView.as_view(month_format="%m"),
        name="archive_month_numeric",
    ),
    # Example: /2012/aug/
    path(
        "<int:year>/<str:month>/",
        ArticleMonthArchiveView.as_view(),
        name="archive_month",
    ),
]
```

Example myapp/article_archive_month.html:

```html
<ul>
    {% for article in object_list %}
        <li>{{ article.pub_date|date:"F j, Y" }}: {{ article.title }}</li>
    {% endfor %}
</ul>

<p>
    {% if previous_month %}
        Previous Month: {{ previous_month|date:"F Y" }}
    {% endif %}
    {% if next_month %}
        Next Month: {{ next_month|date:"F Y" }}
    {% endif %}
</p>
```

## 4. WeekArchiveView

```python
class WeekArchiveView
```

A weekly archive page showing all objects in a given week. Objects with a date in the future are not displayed unless you set allow_future to True.

Ancestors (MRO)

```python
django.views.generic.list.MultipleObjectTemplateResponseMixin
django.views.generic.base.TemplateResponseMixin
django.views.generic.dates.BaseWeekArchiveView
django.views.generic.dates.YearMixin
django.views.generic.dates.WeekMixin
django.views.generic.dates.BaseDateListView
django.views.generic.list.MultipleObjectMixin
django.views.generic.dates.DateMixin
django.views.generic.base.View
```

Context

In addition to the context provided by MultipleObjectMixin (via BaseDateListView), the template’s context will be:

```text
week: A date object representing the first day of the given week.
next_week: A date object representing the first day of the next week, according to
allow_empty and allow_future.
previous_week: A date object representing the first day of the previous week, according to allow_empty and allow_future.
```

Notes

Uses a default `template_name_suffix` of `_archive_week`.
The `week_format` attribute is a `strptime()` format string used to parse the week number. The following values are supported:

*`'%U'`*: Based on the United States week system where the week begins on Sunday. This is the default value.
*`'%W'`*: Similar to *`'%U'`*, except it assumes that the week begins on Monday. This is not the same as the ISO 8601 week number.
*`'%V'`*: ISO 8601 week number where the week begins on Monday.

Example myapp/views.py:

```python
from django.views.generic.dates import WeekArchiveView

from myapp.models import Article

class ArticleWeekArchiveView(WeekArchiveView):
    queryset = Article.objects.all()
    date_field = "pub_date"
    week_format = "%W"
    allow_future = True
```

Example myapp/urls.py:

```python
from django.urls import path

from myapp.views import ArticleWeekArchiveView

urlpatterns = [
    # Example: /2012/week/23/
    path(
        "<int:year>/week/<int:week>/",
        ArticleWeekArchiveView.as_view(),
        name="archive_week",
    ),
]
```

Example myapp/article_archive_week.html:

```html
<h1>Week {{ week|date:'W' }}</h1>

<ul>
    {% for article in object_list %}
        <li>{{ article.pub_date|date:"F j, Y" }}: {{ article.title }}</li>
    {% endfor %}
</ul>

<p>
    {% if previous_week %}
        Previous Week: {{ previous_week|date:"W" }} of year {{ previous_week|date:"Y" }}
    {% endif %}
    {% if previous_week and next_week %}--{% endif %}
    {% if next_week %}
        Next week: {{ next_week|date:"W" }} of year {{ next_week|date:"Y" }}
    {% endif %}
</p>
```

## 5. DayArchiveView

```pythom
class DayArchiveView
```

A day archive page showing all objects in a given day. Days in the future throw a 404 error, regardless of whether any objects exist for future days, unless you set allow_future to True.

Ancestors (MRO)

```python
django.views.generic.list.MultipleObjectTemplateResponseMixin
django.views.generic.base.TemplateResponseMixin
django.views.generic.dates.BaseDayArchiveView
django.views.generic.dates.YearMixin
django.views.generic.dates.MonthMixin
django.views.generic.dates.DayMixin
django.views.generic.dates.BaseDateListView
django.views.generic.list.MultipleObjectMixin
django.views.generic.dates.DateMixin
django.views.generic.base.View
```

Context

In addition to the context provided by MultipleObjectMixin (via BaseDateListView), the template’s context will be:

```text
day: A date object representing the given day.

next_day: A date object representing the next day, according to allow_empty and allow_future.

previous_day: A date object representing the previous day, according to allow_empty and allow_future.

next_month: A date object representing the first day of the next month, according to allow_empty and allow_future.

previous_month: A date object representing the first day of the previous month, according to allow_empty and allow_future.
```

Notes

Uses a default *`template_name_suffix`* of *`_archive_day`*.
Example myapp/views.py:

```python
from django.views.generic.dates import DayArchiveView

from myapp.models import Article

class ArticleDayArchiveView(DayArchiveView):
    queryset = Article.objects.all()
    date_field = "pub_date"
    allow_future = True
```

Example myapp/urls.py:

```python
from django.urls import path

from myapp.views import ArticleDayArchiveView

urlpatterns = [
    # Example: /2012/nov/10/
    path(
        "<int:year>/<str:month>/<int:day>/",
        ArticleDayArchiveView.as_view(),
        name="archive_day",
    ),
]
```

Example myapp/article_archive_day.html:

```html
<h1>{{ day }}</h1>

<ul>
    {% for article in object_list %}
        <li>{{ article.pub_date|date:"F j, Y" }}: {{ article.title }}</li>
    {% endfor %}
</ul>

<p>
    {% if previous_day %}
        Previous Day: {{ previous_day }}
    {% endif %}
    {% if previous_day and next_day %}--{% endif %}
    {% if next_day %}
        Next Day: {{ next_day }}
    {% endif %}
</p>
```

## 6. TodayArchiveView

```python
class TodyArchiveView
```

A day archive page showing all objects for today. This is exactly the same as django.views.generic.dates.DayArchiveView, except today’s date is used instead of the year/month/day arguments.

Ancestors (MRO)

```python
django.views.generic.list.MultipleObjectTemplateResponseMixin
django.views.generic.base.TemplateResponseMixin
django.views.generic.dates.BaseTodayArchiveView
django.views.generic.dates.BaseDayArchiveView
django.views.generic.dates.YearMixin
django.views.generic.dates.MonthMixin
django.views.generic.dates.DayMixin
django.views.generic.dates.BaseDateListView
django.views.generic.list.MultipleObjectMixin
django.views.generic.dates.DateMixin
django.views.generic.base.View
```

Notes

Uses a default *`template_name_suffix`* of *`_archive_today`*.
Example myapp/views.py:

```python
from django.views.generic.dates import TodayArchiveView

from myapp.models import Article

class ArticleTodayArchiveView(TodayArchiveView):
    queryset = Article.objects.all()
    date_field = "pub_date"
    allow_future = True
```

Example myapp/urls.py:

```python
from django.urls import path

from myapp.views import ArticleTodayArchiveView

urlpatterns = [
    path("today/", ArticleTodayArchiveView.as_view(), name="archive_today"),
]
```

Example myapp/article_archive_today.html

```html
<h1>{{ day }}</h1>

<ul>
    {% for article in object_list %}
        <li>{{ article.pub_date|date:"F j, Y" }}: {{ article.title }}</li>
    {% endfor %}
</ul>

<p>
    {% if previous_day %}
        Previous Day: {{ previous_day }}
    {% endif %}
    {% if previous_day and next_day %}--{% endif %}
    {% if next_day %}
        Next Day: {{ next_day }}
    {% endif %}
</p>
```

## 7. DateDetailView

```python
class DateDetailView
```

A page representing an individual object. If the object has a date value in the future, the view will throw a 404 error by default, unless you set allow_future to True.

Ancestors (MRO)

```python
django.views.generic.detail.SingleObjectTemplateResponseMixin
django.views.generic.base.TemplateResponseMixin
django.views.generic.dates.BaseDateDetailView
django.views.generic.dates.YearMixin
django.views.generic.dates.MonthMixin
django.views.generic.dates.DayMixin
django.views.generic.dates.DateMixin
django.views.generic.detail.BaseDetailView
django.views.generic.detail.SingleObjectMixin
django.views.generic.base.View
```

Context

Includes the single object associated with the model specified in the DateDetailView.
Notes

Uses a default *`template_name_suffix`* of *`_detail`*.
Example myapp/urls.py:

```python
from django.urls import path
from django.views.generic.dates import DateDetailView

urlpatterns = [
    path(
        "<int:year>/<str:month>/<int:day>/<int:pk>/",
        DateDetailView.as_view(model=Article, date_field="pub_date"),
        name="archive_date_detail",
    ),
]
```

Example myapp/article_detail.html:

```html
<h1>{{ object.title }}</h1>
```

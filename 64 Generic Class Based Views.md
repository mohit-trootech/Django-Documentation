<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet"/>

# class-based generic views

Generic views are django one of the feature that ease the developer work to write uneccesary code again and again.

Views for listing models data, form handling are most common task by views django, provides generic view class to help developer to ease their pain.

Django ships with generic views to do the following:

1. Display list and detail pages for a single object. If we were creating an application to manage conferences then a TalkListView and a RegisteredUserListView would be examples of list views. A single talk page is an example of what we call a “detail” view.
2. Present date-based objects in year/month/day archive pages, associated detail, and “latest” pages.
3. Allow users to create, update, and delete objects – with or without authorization.
Taken together, these views provide interfaces to perform the most common tasks developers encounter.

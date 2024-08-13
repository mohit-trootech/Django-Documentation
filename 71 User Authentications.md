<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet"/>

# Django Authentication System

Django's authentication system is a robust framework that provides tools for managing users, permissions, and authentication in web applications. This guide covers the essential aspects of Django authentication with examples and real-life applications.

## User Objects

Django provides a `User` model in the `django.contrib.auth` module for handling user accounts.

**Example:**

```python
from django.contrib.auth.models import User

# Create a new user
user = User.objects.create_user(username='john_doe', password='securepassword')
```

**Real-life Application:**

- A user registration system where users can create accounts to access certain features of an application.

## Creating Users

To create users programmatically, you use the `create_user` method which automatically handles password hashing.

**Example:**

```python
user = User.objects.create_user(username='jane_doe', password='mypassword')
```

**Real-life Application:**

- Automated scripts for onboarding new users in a web application.

## Creating Superusers

Superusers have admin privileges and can access the Django admin site.

**Example:**

```bash
python manage.py createsuperuser
```

**Real-life Application:**

- Admins need superuser privileges to manage users, view logs, and access all parts of the admin interface.

## Changing Passwords

Users can change their passwords through the Django admin interface or programmatically.

**Example:**

```python
user = User.objects.get(username='jane_doe')
user.set_password('newpassword')
user.save()
```

**Real-life Application:**

- Users can update their passwords from their profile settings for improved security.

## Authenticating Users

Authentication verifies a user’s identity.

**Example:**

```python
from django.contrib.auth import authenticate

user = authenticate(username='john_doe', password='securepassword')
if user is not None:
    # User is authenticated
    login(request, user)
else:
    # Invalid credentials
```

**Real-life Application:**

- Login functionality in web applications to ensure only authorized users can access their accounts.

## Permissions and Authorization

Permissions control what users can and cannot do in an application.

### Default Permissions

Django provides default permissions for add, change, and delete operations.

**Example:**

```python
from django.contrib.auth.models import Permission

# List default permissions
permissions = Permission.objects.all()
```

**Real-life Application:**

- Admin users can manage objects, while regular users have limited access.

### Groups

Groups allow you to manage permissions for a set of users.

**Example:**

```python
from django.contrib.auth.models import Group

# Create a new group
group = Group.objects.create(name='Editors')

# Assign permissions to a group
permission = Permission.objects.get(codename='change_article')
group.permissions.add(permission)
```

**Real-life Application:**

- Assigning roles like "Editors" or "Viewers" to manage permissions efficiently.

### Programmatically Creating Permissions

You can create custom permissions for your models.

**Example:**

```python
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

# Create custom permission
content_type = ContentType.objects.get_for_model(MyModel)
permission = Permission.objects.create(
    codename='can_publish',
    name='Can publish content',
    content_type=content_type,
)
```

**Real-life Application:**

- Custom permissions for specific actions, like approving content submissions.

### Permission Caching

Django caches permissions to improve performance.

**Example:**

```python
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission

# Access user permissions
user = User.objects.get(username='john_doe')
permissions = user.user_permissions.all()
```

**Real-life Application:**

- Ensures quick permission checks during authentication without hitting the database repeatedly.

## Proxy Models

Proxy models allow you to create different behaviors or interfaces for the same underlying database table.

**Example:**

```python
from django.db import models

class UserProxy(User):
    class Meta:
        ordering = ['username']
        proxy = True
```

**Real-life Application:**

- Create admin interfaces or reporting features without altering the original model.

## Authentication in Web Requests

### How to Log a User In

Use Django's `login` function to authenticate and log users in.

**Example:**

```python
from django.contrib.auth import login

def my_login_view(request):
    user = authenticate(username='john_doe', password='securepassword')
    if user is not None:
        login(request, user)
        return redirect('home')
```

**Real-life Application:**

- Custom login views for user authentication.

### Selecting the Authentication Backend

Specify which backend to use in your `settings.py`.

**Example:**

```python
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default
]
```

**Real-life Application:**

- Use different authentication methods like OAuth or LDAP.

### How to Log a User Out

Use Django's `logout` function to end the user session.

**Example:**

```python
from django.contrib.auth import logout

def my_logout_view(request):
    logout(request)
    return redirect('home')
```

**Real-life Application:**

- Custom logout functionality to end user sessions securely.

## Limiting Access to Logged-in Users

### The Raw Way

Manually check if a user is authenticated.

**Example:**

```python
if request.user.is_authenticated:
    # Access granted
else:
    return redirect('login')
```

**Real-life Application:**

- Custom view logic to restrict access to certain pages.

### The `login_required` Decorator

Use the `login_required` decorator to protect views.

**Example:**

```python
from django.contrib.auth.decorators import login_required

@login_required
def my_view(request):
    return render(request, 'template.html')
```

**Real-life Application:**

- Restrict access to user-specific pages like dashboards.

### The `LoginRequiredMixin` Mixin

Use `LoginRequiredMixin` for class-based views.

**Example:**

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class MyView(LoginRequiredMixin, TemplateView):
    template_name = 'template.html'
```

**Real-life Application:**

- Ensure that class-based views are accessible only to logged-in users.

### Limiting Access to Logged-in Users that Pass a Test

Use `user_passes_test` decorator to restrict access based on custom conditions.

**Example:**

```python
from django.contrib.auth.decorators import user_passes_test

def check_is_admin(user):
    return user.is_staff

@user_passes_test(check_is_admin)
def my_view(request):
    return render(request, 'template.html')
```

**Real-life Application:**

- Allow access based on additional conditions, like user role or status.

### The `permission_required` Decorator

Use the `permission_required` decorator to check for specific permissions.

**Example:**

```python
from django.contrib.auth.decorators import permission_required

@permission_required('app.change_model', raise_exception=True)
def my_view(request):
    return render(request, 'template.html')
```

**Real-life Application:**

- Ensure users have the right permissions to perform certain actions.

### The `PermissionRequiredMixin` Mixin

Use `PermissionRequiredMixin` for class-based views.

**Example:**

```python
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView

class MyView(PermissionRequiredMixin, TemplateView):
    permission_required = 'app.change_model'
    template_name = 'template.html'
```

**Real-life Application:**

- Ensure class-based views are accessible only to users with specific permissions.

### Redirecting Unauthorized Requests in Class-Based Views

Handle unauthorized access in class-based views by overriding methods.

**Example:**

```python
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

class MyView(PermissionRequiredMixin, TemplateView):
    permission_required = 'app.change_model'
    template_name = 'template.html'

    def handle_no_permission(self):
        return redirect('no_permission')
```

**Real-life Application:**

- Customize unauthorized access handling, such as redirecting to an error page.

## Session Invalidation on Password Change

Automatically log out other sessions when a user changes their password.

**Example:**

```python
from django.contrib.auth.models import User

def change_password(user, new_password):
    user.set_password(new_password)
    user.save()
    update_session_auth_hash(request, user)
```

**Real-life Application:**

- Enhance security by invalidating sessions after a password change.

## Authentication Views

Django provides built-in views for authentication tasks.

### Using the Views

Use built-in views for login, logout, and password management.

**Example:**

```python
from django.contrib.auth import views as auth_views

# Login view
path('login/', auth_views.LoginView.as_view(), name='login'),
```

**Real-life Application:**

- Quickly implement standard authentication features.

### All Authentication Views

Django offers views for login, logout, password reset, and password change.

**Example:**

```python
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_change/', auth_views
```

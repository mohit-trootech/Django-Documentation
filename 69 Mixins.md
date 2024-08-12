<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet"/>

# Django Class-Based Mixins

Django's Class-Based Views (CBVs) offer a variety of mixins to handle different aspects of view functionality. Below is a comprehensive guide covering various mixins including editing, date handling, and more.

## **Common Mixins**

### **1. `LoginRequiredMixin`**

**Purpose:** Ensure the user is authenticated before accessing the view.

**Usage:**

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

class MyListView(LoginRequiredMixin, ListView):
    model = MyModel
    template_name = 'my_template.html'
```

**Attributes:**

- `login_url`: URL to redirect unauthenticated users.
- `redirect_field_name`: Query parameter name for redirect URL.

**Methods:**

- `dispatch(request, *args, **kwargs)`

### **2. `PermissionRequiredMixin`**

**Purpose:** Ensure the user has specific permissions to access the view.

**Usage:**

```python
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DetailView

class MyDetailView(PermissionRequiredMixin, DetailView):
    model = MyModel
    template_name = 'my_template.html'
    permission_required = 'app_name.view_mymodel'
```

**Attributes:**

- `permission_required`: Required permission string.
- `raise_exception`: Raise `PermissionDenied` if the user lacks permissions.

**Methods:**

- `dispatch(request, *args, **kwargs)`

### **3. `UserPassesTestMixin`**

**Purpose:** Allow custom test conditions for user access.

**Usage:**

```python
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView

class MyCustomView(UserPassesTestMixin, TemplateView):
    template_name = 'my_template.html'

    def test_func(self):
        return self.request.user.is_staff
```

**Attributes:**

- `login_url`: URL to redirect if test fails.
- `raise_exception`: Raise `PermissionDenied` if test fails.

**Methods:**

- `test_func()`

### **1. `ContextMixin`**

**Purpose:** Provides a way to pass additional context data to the template.

**Usage:**

```python
from django.views.generic.base import ContextMixin
from django.views.generic import TemplateView

class MyContextView(ContextMixin, TemplateView):
    template_name = 'my_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_var'] = 'Hello, World!'
        return context
```

**Methods:**

- `get_context_data(**kwargs)`: Returns the context data for the template.

### **2. `TemplateResponseMixin`**

**Purpose:** Provides a way to render templates with context data.

**Usage:**

```python
from django.views.generic.base import TemplateResponseMixin
from django.views.generic import View

class MyTemplateView(TemplateResponseMixin, View):
    template_name = 'my_template.html'

    def get(self, request, *args, **kwargs):
        context = {'my_var': 'Hello, World!'}
        return self.render_to_response(context)
```

**Methods:**

- `render_to_response(context)`: Renders the template with the given context.

## **Single Object Mixins**

### **3. `SingleObjectMixin`**

**Purpose:** Provides functionality to retrieve a single object based on primary key or slug.

**Usage:**

```python
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View
from .models import MyModel

class MySingleObjectView(SingleObjectMixin, View):
    model = MyModel

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_response({'object': self.object})
```

**Attributes:**

- `model`: Model class to retrieve.
- `pk_url_kwarg`: URL keyword argument for primary key.
- `slug_url_kwarg`: URL keyword argument for slug.

**Methods:**

- `get_object()`

### **4. `SingleObjectTemplateResponseMixin`**

**Purpose:** Combines `SingleObjectMixin` with template rendering.

**Usage:**

```python
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic import View
from .models import MyModel

class MySingleObjectTemplateView(SingleObjectTemplateResponseMixin, View):
    model = MyModel
    template_name = 'my_template.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
```

**Methods:**

- `get_context_data(**kwargs)`: Returns context data for the template.

## **Multiple Object Mixins**

### **5. `MultipleObjectMixin`**

**Purpose:** Provides functionality to handle multiple objects, such as lists.

**Usage:**

```python
from django.views.generic.list import MultipleObjectMixin
from django.views.generic import View
from .models import MyModel

class MyMultipleObjectView(MultipleObjectMixin, View):
    model = MyModel

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return self.render_to_response({'object_list': self.object_list})
```

**Attributes:**

- `queryset`: Queryset of objects to retrieve.

**Methods:**

- `get_queryset()`

### **6. `MultipleObjectTemplateResponseMixin`**

**Purpose:** Combines `MultipleObjectMixin` with template rendering.

**Usage:**

```python
from django.views.generic.list import MultipleObjectTemplateResponseMixin
from django.views.generic import View
from .models import MyModel

class MyMultipleObjectTemplateView(MultipleObjectTemplateResponseMixin, View):
    model = MyModel
    template_name = 'my_template.html'

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)
        return self.render_to_response(context)
```

**Methods:**

- `get_context_data(**kwargs)`: Returns context data for the template.

## **Editing Mixins**

### **7. `FormMixin`**

**Purpose:** Provides form handling for views.

**Usage:**

```python
from django.views.generic.edit import FormMixin
from django.views.generic import View
from .forms import MyForm

class MyFormView(FormMixin, View):
    form_class = MyForm

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        return self.render_to_response({'form': form})

    def form_valid(self, form):
        # Handle form validation success
        return super().form_valid(form)
```

**Attributes:**

- `form_class`: Form class to use.

**Methods:**

- `get_form()`
- `get_form_class()`
- `form_valid(form)`

### **8. `ModelFormMixin`**

**Purpose:** Provides functionality for views that work with model forms.

**Usage:**

```python
from django.views.generic.edit import ModelFormMixin
from django.views.generic import View
from .forms import MyModelForm

class MyModelFormView(ModelFormMixin, View):
    form_class = MyModelForm

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        return self.render_to_response({'form': form})

    def form_valid(self, form):
        # Handle form validation success
        return super().form_valid(form)
```

**Attributes:**

- `form_class`: Model form class to use.

**Methods:**

- `get_form()`
- `get_form_class()`
- `form_valid(form)`

### **9. `ProcessFormView`**

**Purpose:** Base class for processing forms.

**Usage:**

```python
from django.views.generic.edit import ProcessFormView
from .forms import MyForm

class MyProcessFormView(ProcessFormView):
    form_class = MyForm
    template_name = 'my_template.html'
    success_url = '/success/'

    def form_valid(self, form):
        # Handle form validation success
        return super().form_valid(form)
```

**Attributes:**

- `form_class`: Form class to use.
- `success_url`: URL to redirect after a successful form submission.

**Methods:**

- `form_valid(form)`
- `form_invalid(form)`

### **10. `DeletionMixin`**

**Purpose:** Provides functionality for deleting an object.

**Usage:**

```python
from django.views.generic.edit import DeleteView
from .models import MyModel

class MyDeleteView(DeleteView):
    model = MyModel
    template_name = 'confirm_delete.html'
    success_url = '/success/'
```

**Attributes:**

- `model`: Model class to delete.
- `template_name`: Template for confirming deletion.
- `success_url`: URL to redirect after successful deletion.

**Methods:**

- `delete(request, *args, **kwargs)`

## **Date-Based Mixins**

### **11. `YearMixin`**

**Purpose:** Provides functionality for filtering objects by year.

**Usage:**

```python
from django.views.generic.list import ListView
from django.utils import timezone
from .models import MyModel

class MyYearView(ListView):
    model = MyModel

    def get_queryset(self):
        year = self.kwargs.get('year', timezone.now().year)
        return MyModel.objects.filter(date_field__year=year)
```

**Attributes:**

- `year`: Year to filter objects by.

**Methods:**

- `get_queryset()`

### **12. `MonthMixin`**

**Purpose:** Provides functionality for filtering objects by month.

**Usage:**

```python
from django.views.generic.list import ListView
from django.utils import timezone
from .models import MyModel

class MyMonthView(ListView):
    model = MyModel

    def get_queryset(self):
        year = self.kwargs.get('year', timezone.now().year)
        month = self.kwargs.get('month', timezone.now().month)
        return MyModel.objects.filter(date_field__year=year, date_field__month=month)
```

**Attributes:**

- `year`: Year to filter objects by.
- `month`: Month to filter objects by.

**Methods:**

- `get_queryset()`

### **13. `DayMixin`**

**Purpose:** Provides functionality for filtering objects by day.

**Usage:**

```python
from django.views.generic.list import ListView
from django.utils import timezone
from .models import MyModel

class MyDayView(ListView):
    model = MyModel

    def get_queryset(self):
        year = self.kwargs.get('year', timezone.now().year)
        month = self.kwargs.get('month', timezone.now().month)
        day = self.kwargs.get('day', timezone.now().day)
        return MyModel.objects.filter(date_field__year=year, date_field__month=month, date_field__day=day)
```

**Attributes:**

- `year`: Year to filter objects by.
- `month`: Month to filter objects by.
- `day`: Day to filter objects by.

**Methods:**

- `get_queryset()`

### **14. `WeekMixin`**

**Purpose:** Provides functionality for filtering objects by week.

**Usage:**

```python


from django.views.generic.list import ListView
from django.utils import timezone
from .models import MyModel
from django.db.models.functions import TruncWeek

class MyWeekView(ListView):
    model = MyModel

    def get_queryset(self):
        year = self.kwargs.get('year', timezone.now().year)
        week = self.kwargs.get('week', timezone.now().isocalendar()[1])
        return MyModel.objects.annotate(week=TruncWeek('date_field')).filter(date_field__year=year, week=week)
```

**Attributes:**

- `year`: Year to filter objects by.
- `week`: Week number to filter objects by.

**Methods:**

- `get_queryset()`

### **15. `DateMixin`**

**Purpose:** Provides date-based filtering functionality.

**Usage:**

```python
from django.views.generic.list import ListView
from django.utils import timezone
from .models import MyModel

class MyDateView(ListView):
    model = MyModel

    def get_queryset(self):
        start_date = self.kwargs.get('start_date')
        end_date = self.kwargs.get('end_date')
        return MyModel.objects.filter(date_field__range=[start_date, end_date])
```

**Attributes:**

- `start_date`: Start date for filtering.
- `end_date`: End date for filtering.

**Methods:**

- `get_queryset()`

### **16. `BaseDateListView`**

**Purpose:** A base view for date-based lists.

**Usage:**

```python
from django.views.generic.dates import BaseDateListView
from .models import MyModel

class MyBaseDateListView(BaseDateListView):
    model = MyModel
    date_field = 'date_field'
    template_name = 'my_template.html'

    def get_queryset(self):
        return MyModel.objects.all()
```

**Attributes:**

- `date_field`: Field on the model that stores date information.

**Methods:**

- `get_queryset()`

## **Combining Mixins**

Mixins can be combined in various ways to create complex views with multiple functionalities. Ensure that mixins are listed in the correct order, as Python uses method resolution order (MRO) to determine which method to use.

**Example:**

```python
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView
from .models import MyModel
from .forms import MyModelForm

class MySecureCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = MyModel
    form_class = MyModelForm
    template_name = 'my_template.html'
    success_url = '/success/'
    permission_required = 'app_name.add_mymodel'
```

In this example, the view requires the user to be logged in and have a specific permission to create a new object.

---

This comprehensive guide should cover most of the commonly used mixins in Django and their applications.

<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet"/>

# Django Migrations

## Overview

Django migrations are a way of managing changes to your database schema in a systematic and organized manner. They ensure that the database schema remains consistent with your Django models.

## Key Concepts

### 1. Migrations

- **Definition**: Migrations are Django's way of propagating changes you make to your models into the database schema.
- **Usage**: Use `makemigrations` to create migration files and `migrate` to apply them.

  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

### 2. Commands

- **`makemigrations`**: Generates new migration files based on changes detected in your models.

  ```bash
  python manage.py makemigrations
  ```

- **`migrate`**: Applies the migrations to your database.

  ```bash
  python manage.py migrate
  ```

- **`showmigrations`**: Displays a list of migrations and their status.

  ```bash
  python manage.py showmigrations
  ```

- **`sqlmigrate`**: Shows the SQL commands that will be executed for a particular migration.

  ```bash
  python manage.py sqlmigrate myapp 0001
  ```

### 3. Backend Support

Django supports various database backends:

- **PostgreSQL**
- **MySQL**
- **SQLite**
- **Oracle**

**Note**: Some features, such as full-text search or JSON fields, may be specific to certain database backends.

### 4. Workflow

1. **Create Models**: Define or modify your Django models in `models.py`.

2. **Generate Migrations**: Run `makemigrations` to create migration files reflecting your model changes.

3. **Apply Migrations**: Run `migrate` to apply the migrations to your database.

  ```bash
  # Example of creating a model
  from django.db import models

  class Author(models.Model):
      name = models.CharField(max_length=100)

  # Example of generating and applying migrations
  python manage.py makemigrations
  python manage.py migrate
  ```

### 5. Transactions

- **Transactional Migrations**: Migrations are generally wrapped in a transaction, ensuring atomicity. If an error occurs, changes are rolled back.

- **Example**: If a migration creates a table and adds a column, both operations will either complete successfully or not at all.

### 6. Dependencies

- **Migration Dependencies**: Ensure migrations are applied in the correct order by defining dependencies.

  ```python
  class Migration(migrations.Migration):
      dependencies = [
          ('myapp', '0001_initial'),
      ]
  ```

### 7. Swappable Dependencies

- **Swappable Models**: Use Django’s `get_model` method to refer to models that can be swapped out.

  ```python
  from django.apps import apps

  def forwards(apps, schema_editor):
      MyModel = apps.get_model('myapp', 'MyModel')
  ```

### 8. Migration Fields

- **Field Operations**: Add, remove, or alter fields in your models.

  ```python
  class Migration(migrations.Migration):
      operations = [
          migrations.AddField(
              model_name='author',
              name='birthdate',
              field=models.DateField(null=True, blank=True),
          ),
      ]
  ```

### 9. Custom Fields

- **Defining Custom Fields**: Extend Django’s built-in fields with your own.

  ```python
  from django.db import models

  class UpperCaseCharField(models.CharField):
      def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)

      def deconstruct(self):
          name, path, args, kwargs = super().deconstruct()
          return name, path, args, kwargs
  ```

### 10. Model Managers in Migrations

- **Manager Usage**: Model managers handle queries and are not directly involved in migrations but can be used in data migrations.

  ```python
  from django.db import migrations

  def forwards(apps, schema_editor):
      Author = apps.get_model('myapp', 'Author')
      Author.objects.create(name='John Doe')
  ```

### 11. Initial Migrations

- **Purpose**: Create the initial schema for an app.

  ```bash
  python manage.py makemigrations myapp
  ```

- **Automatic Creation**: Django generates an initial migration when you first create a model.

### 12. History Consistency

- **Migration History**: Django maintains a history of applied migrations in the `django_migrations` table to ensure consistency.

### 13. Reversing Migrations

- **Rollback**: Use `migrate <app_name> <migration_name>` to roll back to a previous migration state.

  ```bash
  python manage.py migrate myapp 0001
  ```

- **Reversibility**: Not all migrations can be reversed. Implement custom methods to handle non-reversible changes.

### 14. Data Migration

- **Purpose**: Migrate data in conjunction with schema changes.

  ```python
  from django.db import migrations

  def forwards(apps, schema_editor):
      Author = apps.get_model('myapp', 'Author')
      for author in Author.objects.all():
          author.name = author.name.upper()
          author.save()

  class Migration(migrations.Migration):
      operations = [
          migrations.RunPython(forwards),
      ]
  ```

### 15. Squashing Migrations

- **Definition**: Combine multiple migration files into a single file to reduce clutter.

  ```bash
  python manage.py squashmigrations myapp 0001 0005
  ```

### 16. Serializing Values

- **Serialization**: Convert model data to and from formats suitable for storage or transmission.

  ```python
  def serialize(value):
      return str(value)

  def deserialize(value):
      return int(value)
  ```

### 17. Custom Serializers

- **Custom Serializers**: Implement `deconstruct` and `from_db_value` methods to handle custom serialization.

  ```python
  class MyCustomField(models.Field):
      def deconstruct(self):
          name, path, args, kwargs = super().deconstruct()
          return name, path, args, kwargs

      def from_db_value(self, value, expression, connection, context):
          return value
  ```

### 18. Deconstruct()

- **Purpose**: Serialize field or model definitions into a format for migrations.

  ```python
  class MyCustomField(models.Field):
      def deconstruct(self):
          name, path, args, kwargs = super().deconstruct()
          return name, path, args, kwargs
  ```

### 19. Zero Migrations

- **Definition**: A migration with zero operations, often used to mark a point in the migration history.

  ```python
  class Migration(migrations.Migration):
      operations = []
  ```

### 20. Fake Migrations

- **Definition**: Mark a migration as applied without executing it.

  ```bash
  python manage.py migrate --fake myapp 0001
  ```

### 21. Fake Initial Migrations

- **Purpose**: Mark initial migrations as applied without creating or applying them.

  ```bash
  python manage.py migrate --fake-initial
  ```

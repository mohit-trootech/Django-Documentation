<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet" />

# FieldTypes

## 1. AutoField

An IntegerField that automatically increments according to available IDs. You usually won’t need to use this directly; a primary key field will automatically be added to your model if you don’t specify otherwise.

## 2. BigAutoField

A 64-bit integer, much like an AutoField except that it is guaranteed to fit numbers from 1 to 9223372036854775807.

## 3. BigIntegerField

A 64-bit integer, much like an IntegerField except that it is guaranteed to fit numbers from -9223372036854775808 to 9223372036854775807. *The default form widget for this field is a NumberInput.*

## 4. BinaryField

A field to store raw binary data. It can be assigned bytes, bytearray, or memoryview.

By default, BinaryField sets editable to False, in which case it can’t be included in a ModelForm.

### BinaryField.max_length

Optional. The maximum length (in bytes) of the field. The maximum length is enforced in Django’s validation using MaxLengthValidator.

## 5. BooleanField

A true/false field.

The default form widget for this field is CheckboxInput, or NullBooleanSelect if null=True.

The default value of BooleanField is None when Field.default isn’t defined.

## 6. CharField

A string field, for small- to large-sized strings.

For large amounts of text, use `TextField`.

The default form widget for this field is a TextInput.

### CharField.max_length

The maximum length (in characters) of the field. The `max_length` is enforced at the database level and in Django’s validation using `MaxLengthValidator`.

## 7. DateField

    DateField(auto_now=False, auto_now_add=False, **options)
A date, represented in Python by a datetime.date instance. Has a few extra, optional arguments:

### DateField.auto_now

Automatically set the field to now every time the object is saved. Useful for “last-modified” timestamps. Note that the current date is always used; it’s not just a default value that you can override.

The field is only automatically updated when calling Model.save(). The field isn’t updated when making updates to other fields in other ways such as QuerySet.update(), though you can specify a custom value for the field in an update like that.

### DateField.auto_now_add

Automatically set the field to now when the object is first created. Useful for creation of timestamps. Note that the current date is always used; it’s not just a default value that you can override. So even if you set a value for this field when creating the object, it will be ignored. If you want to be able to modify this field, set the following instead of auto_now_add=True:

## 8. DateTimeField

    DateTimeField(auto_now=False, auto_now_add=False, **options)
A date and time, represented in Python by a datetime.datetime instance. Takes the same extra arguments as DateField.

The default form widget for this field is a single DateTimeInput. The admin uses two separate TextInput widgets with JavaScript shortcuts.

## 9. DecimalField

    DecimalField(max_digits=None, decimal_places=None, **options)
A fixed-precision decimal number, represented in Python by a Decimal instance. It validates the input using DecimalValidator.

### DecimalField.max_digits

The maximum number of digits allowed in the number. Note that this number must be greater than or equal to decimal_places.

### DecimalField.decimal_places

The number of decimal places to store with the number.

For example, to store numbers up to 999.99 with a resolution of 2 decimal places, you’d use:

    models.DecimalField(..., max_digits=5, decimal_places=2)
And to store numbers up to approximately one billion with a resolution of 10 decimal places:

    models.DecimalField(..., max_digits=19, decimal_places=10)

## 10. FloatField

    FloatField(**options)
A floating-point number represented in Python by a float instance.

The default form widget for this field is a NumberInput when localize is False or TextInput otherwise.

## 11. DurationField

    DurationField(**options)
A field for storing periods of time - modeled in Python by timedelta. When used on PostgreSQL, the data type used is an interval and on Oracle the data type is INTERVAL DAY(9) TO SECOND(6). Otherwise a bigint of microseconds is used.

## 12. EmailField

    EmailField(max_length=254, **options)
A CharField that checks that the value is a valid email address using EmailValidator.

## 13. FileField

    FileField(upload_to='', storage=None, max_length=100, **options)
A file-upload field.

### FileField.upload_to

This attribute provides a way of setting the upload directory and file name, and can be set in two ways. In both cases, the value is passed to the Storage.save() method.

    class MyModel(models.Model):
        # file will be uploaded to MEDIA_ROOT/uploads
        upload = models.FileField(upload_to="uploads/")
        # or...
        # file will be saved to MEDIA_ROOT/uploads/2015/01/30
        upload = models.FileField(upload_to="uploads/%Y/%m/%d/")

upload_to may also be a callable, such as a function.

    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return "user_{0}/{1}".format(instance.user.id, filename)

    class MyModel(models.Model):
        upload = models.FileField(upload_to=user_directory_path)

## 14. GenericIPAddressField

    GenericIPAddressField(protocol='both', unpack_ipv4=False, **options)
An IPv4 or IPv6 address, in string format (e.g. 192.0.2.30 or 2a02:42fe::4). The default form widget for this field is a TextInput.

## 15. ImageField

    ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, **options)
Inherits all attributes and methods from FileField, but also validates that the uploaded object is a valid image.

### ImageField.height_field

Name of a model field which will be auto-populated with the height of the image each time the model instance is saved.

### ImageField.width_field

Name of a model field which will be auto-populated with the width of the image each time the model instance is saved.

- *Note: Requires the Pillow library.*

***ImageField instances are created in your database as varchar columns with a default max length of 100 characters. As with other fields, you can change the maximum length using the max_length argument.***

## 16. IntegerField

    IntegerField(**options)
An integer. Values from -2147483648 to 2147483647 are safe in all databases supported by Django.

It uses MinValueValidator and MaxValueValidator to validate the input based on the values that the default database supports.

The default form widget for this field is a NumberInput when localize is False or TextInput otherwise.

## 17. JSONField

    JSONField(encoder=None, decoder=None, **options)¶
A field for storing JSON encoded data. In Python the data is represented in its Python native format: dictionaries, lists, strings, numbers, booleans and None.

JSONField is supported on MariaDB, MySQL, Oracle, PostgreSQL, and SQLite (with the JSON1 extension enabled).

### JSONField.encoder

An optional json.JSONEncoder subclass to serialize data types not supported by the standard JSON serializer (e.g. datetime.datetime or UUID). For example, you can use the DjangoJSONEncoder class.

Defaults to json.JSONEncoder.

### JSONField.decoder

An optional json.JSONDecoder subclass to deserialize the value retrieved from the database. The value will be in the format chosen by the custom encoder (most often a string). Your deserialization may need to account for the fact that you can’t be certain of the input type. For example, you run the risk of returning a datetime that was actually a string that just happened to be in the same format chosen for datetimes.

Defaults to json.JSONDecoder.

## 18. PositiveBigIntegerField

    PositiveBigIntegerField(**options)
Like a PositiveIntegerField, but only allows values under a certain (database-dependent) point. Values from 0 to 9223372036854775807 are safe in all databases supported by Django.

## 19. PositiveIntegerField

    PositiveIntegerField(**options)
Like an IntegerField, but must be either positive or zero (0). Values from 0 to 2147483647 are safe in all databases supported by Django. The value 0 is accepted for backward compatibility reasons.

## 20. PositiveSmallIntegerField

    PositiveSmallIntegerField(**options)
Like a PositiveIntegerField, but only allows values under a certain (database-dependent) point. Values from 0 to 32767 are safe in all databases supported by Django.

## 21. SlugField

    SlugField(max_length=50, **options)
Slug is a newspaper term. A slug is a short label for something, containing only letters, numbers, underscores or hyphens. They’re generally used in URLs.

### SlugField.allow_unicode

If True, the field accepts Unicode letters in addition to ASCII letters. Defaults to False.

## 22. SmallAutoField

    SmallAutoField(**options)
Like an AutoField, but only allows values under a certain (database-dependent) limit. Values from 1 to 32767 are safe in all databases supported by Django.

## 23. SmallIntegerField

    SmallIntegerField(**options)
Like an IntegerField, but only allows values under a certain (database-dependent) point. Values from -32768 to 32767 are safe in all databases supported by Django.

## 24. TextField

    TextField(**options)
A large text field. The default form widget for this field is a Textarea.

If you specify a max_length attribute, it will be reflected in the Textarea widget of the auto-generated form field. However it is not enforced at the model or database level. Use a CharField for that.

## 25. TimeField

    TimeField(auto_now=False, auto_now_add=False, **options)
A time, represented in Python by a datetime.time instance. Accepts the same auto-population options as DateField.

The default form widget for this field is a TimeInput. The admin adds some JavaScript shortcuts.

## 26. URLField

    URLField(max_length=200, **options)
A CharField for a URL, validated by URLValidator.

The default form widget for this field is a URLInput.

Like all CharField subclasses, URLField takes the optional max_length argument. If you don’t specify max_length, a default of 200 is used.

## 27. UUIDField

    UUIDField(**options)
A field for storing universally unique identifiers. Uses Python’s UUID class. When used on PostgreSQL and MariaDB 10.7+, this stores in a uuid datatype, otherwise in a char(32).

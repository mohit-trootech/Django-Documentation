<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet" />

# Model field reference

The following arguments are available to all field types. All are optional.

## null

- If True, Django will store empty values as NULL in the database. Default is False.
- Avoid using null on string-based fields such as CharField and TextField. If a string-based field has null=True,

## blank

- If True, the field is allowed to be blank. Default is False.
- This is different than null. null is purely database-related, whereas blank is validation-related.If a field has blank=True, form validation will allow entry of an empty value. If a field has blank=False, the field will be required.

## choices

A mapping or iterable in the format described below to use as choices for this field. If choices are given, they’re enforced by model validation and the default form widget will be a select box with these choices instead of the standard text field.

    YEAR_IN_SCHOOL_CHOICES = {
        "FR": "Freshman",
        "SO": "Sophomore",
        "JR": "Junior",
        "SR": "Senior",
        "GR": "Graduate",
    }
    OR
    CURRENCIES = [
    ("INR", "Indian Ruppee"),
    ("USD", "US Dollar"),
    ("EU", "Euro"),
    ("DK", "Dhaka"),
    ]

    class Expense(models.Model):
        amount = models.DecimalField(max_digits=10, decimal_places=2)
        currency = models.CharField(max_length=3, choices=    CURRENCIES)

### Meta choices

    MEDIA_CHOICES = [
        (
            "Audio",
            (
                ("vinyl", "Vinyl"),
                ("cd", "CD"),
            ),
        ),
        (
            "Video",
            (
                ("vhs", "VHS Tape"),
                ("dvd", "DVD"),
            ),
        ),
        ("unknown", "Unknown"),
    ]

## db_column

The name of the database column to use for this field. If this isn’t given, Django will use the field’s name.

## db_comment

The comment on the database column to use for this field. It is useful for documenting fields for individuals with direct database access who may not be looking at your Django code. For example:

    pub_date = models.DateTimeField(
        db_comment="Date and time when the article was published",
    )

## db_default

The database-computed default value for this field. This can be a literal value or a database function, such as Now:

    created = models.DateTimeField(db_default=Now())

## db_index

If True, a database index will be created for this field.

## default

    The default value for the field. This can be a value or a callable object. If callable it will be called every time a new object is created.

The default can’t be a mutable object (model instance, list, set, etc.), as a reference to the same instance of that object would be used as the default value in all new model instances. Instead, wrap the desired default in a callable. For example, if you want to specify a default dict for JSONField, use a function:

    def contact_default():
        return {"email": "<to1@example.com>"}

    contact_info = JSONField("ContactInfo", default=contact_default)

## editable

If False, the field will not be displayed in the admin or any other ModelForm. They are also skipped during model validation. Default is True.

## error_messages

The error_messages argument lets you override the default messages that the field will raise. Pass in a dictionary with keys matching the error messages you want to override.

Error message keys include null, blank, invalid, invalid_choice, unique, and unique_for_date. Additional error message keys are specified for each field in the Field types section below.

    ### ModelForm
    from django.core.exceptions import NON_FIELD_ERRORS
    from django.forms import ModelForm

    class ArticleForm(ModelForm):
        class Meta:
            error_messages = {
                NON_FIELD_ERRORS: {
                    "unique_together": "%(model_name)s's %(field_labels)s are not unique.",
                }
            }

## help_text

Extra “help” text to be displayed with the form widget. It’s useful for documentation even if your field isn’t used on a form.

Note that this value is not HTML-escaped in automatically-generated forms. This lets you include HTML in help_text if you so desire. For example:

    help_text = "Please use the following format: <em>YYYY-MM-DD</em>."

## primary_key¶

If True, this field is the primary key for the model.

- *Note this will override default primary_key of the model which is id by default*

## unique

If True, this field must be unique throughout the table.

## unique_for_date

Set this to the name of a DateField or DateTimeField to require that this field be unique for the value of the date field.

For example, if you have a field title that has `unique_for_date="pub_date"`, then Django wouldn’t allow the entry of two records with the same title and pub_date.

- *Note: Similar unique_for_year, unique_for_month*

## verbose_name

A human-readable name for the field. If the verbose name isn’t given, Django will automatically create it using the field’s attribute name, converting underscores to spaces. See Verbose field names.

    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        verbose_name="the related poll",
    )
    sites = models.ManyToManyField(Site, verbose_name="list of sites")
    place = models.OneToOneField(
        Place,
        on_delete=models.CASCADE,
        verbose_name="related place",
    )

## validators

A list of validators to run for this field. See the validators documentation for more information.

- *Note: Will see Validators in Next Module*

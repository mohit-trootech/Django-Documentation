<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet" />

# Validators

A validator is a callable that takes a value and raises a ValidationError if it doesn’t meet some criteria. Validators can be useful for reusing validation logic between different types of fields.

For example, here’s a validator that only allows even numbers:

    from django.core.exceptions import ValidationError
    from django.utils.translation import gettext_lazy as_

    def validate_even(value):
        if value % 2 != 0:
            raise ValidationError(
                _("%(value)s is not an even number"),
                params={"value": value},
            )
You can add this to a model field via the field’s validators argument:

    from django.db import models

    class MyModel(models.Model):
        even_field = models.IntegerField(validators=[validate_even])
Because values are converted to Python before validators are run, you can even use the same validator with forms:

    from django import forms

    class MyForm(forms.Form):
        even_field = forms.IntegerField(validators=[validate_even])

## RegexValidator

    class RegexValidator(regex=None, message=None, code=None, inverse_match=None, flags=0)

Parameters:

1. regex – If not None, overrides regex. Can be a regular expression string or a pre-compiled regular expression.
2. message – If not None, overrides message.
3. code – If not None, overrides code.
4. inverse_match – If not None, overrides inverse_match.
5. flags – If not None, overrides flags. In that case, regex must be a regular expression string, or TypeError is raised.

A RegexValidator searches the provided value for a given regular expression with re.search(). By default, raises a ValidationError with message and code if a match is not found. Its behavior can be inverted by setting inverse_match to True, in which case the ValidationError is raised when a match is found.

## EmailValidator

    EmailValidator(message=None, code=None, allowlist=None)

Parameters:

1. message – If not None, overrides message.
2. code – If not None, overrides code.
3. allowlist – If not None, overrides allowlist.

An EmailValidator ensures that a value looks like an email, and raises a ValidationError with message and code if it doesn’t. Values longer than 320 characters are always considered invalid.

## URLValidator

    URLValidator(schemes=None, regex=None, message=None, code=None)

A RegexValidator subclass that ensures a value looks like a URL, and raises an error code of 'invalid' if it doesn’t. Values longer than max_length characters are always considered invalid.

## validate_email

An EmailValidator instance without any customizations.

## validate_slug

A RegexValidator instance that ensures a value consists of only letters, numbers, underscores or hyphens.

## validate_unicode_slug

A RegexValidator instance that ensures a value consists of only Unicode letters, numbers, underscores, or hyphens.

## validate_ipv4_address

A RegexValidator instance that ensures a value looks like an IPv4 address.

## validate_ipv6_address

Uses django.utils.ipv6 to check the validity of an IPv6 address.

## validate_ipv46_address

Uses both validate_ipv4_address and validate_ipv6_address to ensure a value is either a valid IPv4 or IPv6 address.

## validate_comma_separated_integer_list

A RegexValidator instance that ensures a value is a comma-separated list of integers.

## int_list_validator

    int_list_validator(sep=',', message=None, code='invalid', allow_negative=False)
Returns a RegexValidator instance that ensures a string consists of integers separated by sep. It allows negative integers when allow_negative is True.

## MaxValueValidator

    MaxValueValidator(limit_value, message=None)
Raises a ValidationError with a code of 'max_value' if value is greater than limit_value, which may be a callable.

## MinValueValidator

    MinValueValidator(limit_value, message=None)
Raises a ValidationError with a code of 'min_value' if value is less than limit_value, which may be a callable.

## MaxLengthValidator

    MaxLengthValidator(limit_value, message=None)
Raises a ValidationError with a code of 'max_length' if the length of value is greater than limit_value, which may be a callable.

## MinLengthValidator

    MinLengthValidator(limit_value, message=None)
Raises a ValidationError with a code of 'min_length' if the length of value is less than limit_value, which may be a callable.

## DecimalValidator

    DecimalValidator(max_digits, decimal_places)
Raises ValidationError with the following codes:

1. 'max_digits' if the number of digits is larger than max_digits.
2. 'max_decimal_places' if the number of decimals is larger than decimal_places.
3. 'max_whole_digits' if the number of whole digits is larger than the difference between max_digits and decimal_places.

## FileExtensionValidator

    FileExtensionValidator(allowed_extensions, message, code)
Raises a ValidationError with a code of 'invalid_extension' if the extension of value.name (value is a File) isn’t found in allowed_extensions. The extension is compared case-insensitively with allowed_extensions.

## validate_image_file_extension

Uses Pillow to ensure that value.name (value is a File) has a valid image extension.

## ProhibitNullCharactersValidator

    ProhibitNullCharactersValidator(message=None, code=None)
Raises a ValidationError if str(value) contains one or more null characters ('\x00').

## StepValueValidator

    StepValueValidator(limit_value, message=None, offset=None)
Raises a ValidationError with a code of 'step_size' if value is not an integral multiple of limit_value, which can be a float, integer or decimal value or a callable. When offset is set, the validation occurs against limit_value plus offset.
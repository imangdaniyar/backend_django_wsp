from django.core.exceptions import ValidationError


def validate_university_email(value):
    if "@kbtu.kz" not in value.lower():
        raise ValidationError("A valid KBTU email must be entered in")
    else:
        return value

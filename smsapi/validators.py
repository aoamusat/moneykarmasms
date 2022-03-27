from rest_framework.serializers import ValidationError


def validate_phone_number(value):
    if len(str(value)) < 6:
        raise ValidationError("Phone number is invalid")
    if len(str(value)) > 16:
        raise ValidationError("Phone number is invalid")
    return value


def validate_from(value):
    return value


def validate_to(value):
    return value


def validate_text(value):
    if len(str(value)) < 1:
        raise ValidationError("Text is invalid")
    if len(str(value)) > 120:
        raise ValidationError("Text is invalid")
    return value

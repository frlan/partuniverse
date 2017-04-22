from .models import ValidationError


def validate_file_extension(value):
    try:
        if value.file.content_type != 'application/pdf':
            raise ValidationError(u'Filetyp not supported')
    except AttributeError:
        pass

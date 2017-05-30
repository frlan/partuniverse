from .models import ValidationError


def validate_file_extension(value):
    try:
        if value.file.content_type != 'application/pdf':
            raise ValidationError(u'Filetyp not supported')
    except AttributeError:
        pass

def createExcelArray(rows, cols):
    result = []
    for i in range(0,cols):
        for j in range(0,rows):
            result.append("{}{}".format(chr(ord('A')+i),(j+1)))
    return result



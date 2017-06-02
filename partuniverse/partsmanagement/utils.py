from .models import ValidationError


def validate_file_extension(value):
    try:
        if value.file.content_type != 'application/pdf':
            raise ValidationError(u'Filetyp not supported')
    except AttributeError:
        pass


def convertToBase26(num):
    number = [chr(i) for i in range(65, 91)]
    print
    if num < 26:
        return number[num]
    else:
        return (
            convertToBase26(num // 26 - 1) +
            str((number[num % 26]))
        )


def createExcelArray(rows, cols):
    result = []
    for col in range(0, cols):
        for row in range(1, rows + 1):
            result.append(
                '{}{}'.format(convertToBase26(col), row))
    return result

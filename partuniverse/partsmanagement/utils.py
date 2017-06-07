from .models import ValidationError


def is_pdf(fileob):
    return fileob.content_type == 'application/pdf'


def is_img(fileob):
    return fileob.content_type.startswith('image/')


def validate_file_extension(value):
    try:
        if not (is_pdf(value.file) or is_img(value.file)):
            raise ValidationError(u'Filetype not supported')
    except AttributeError:
        pass


def convertToBase26(num):
    """
    Converts an integer to a Excel-column-like string.
    Example AA, BBZ ...
    """
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
    """
    Creates a list of fields based on given rows and columns
    in Excel-like syntex. Example: AA15
    """
    result = []
    for col in range(0, cols):
        for row in range(1, rows + 1):
            result.append(
                '{}{}'.format(convertToBase26(col), row))
    return result

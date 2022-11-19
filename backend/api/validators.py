from django.core.exceptions import ValidationError
from magic import from_buffer


def image_validator(value):
    allowed_extensions = ['image/jpeg', 'image/png']
    content_type = from_buffer(value.read(1024), mime=True)
    if content_type not in allowed_extensions:
        raise ValidationError(
            'Файл должен иметь разрешение jpeg или png'
            ' и являться изображением.'
        )

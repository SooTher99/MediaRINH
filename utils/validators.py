from rest_framework.serializers import ValidationError
from string import punctuation, digits
from pathlib import Path

import magic
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


def validate_letters(name):
    if not set(name).isdisjoint(punctuation + digits):
        raise ValidationError("Поле должно содержать только буквы")


@deconstructible
class FileMimeValidator:
    """
    Валидация на типы файлов
    """
    messages = {
        "Подозрительный файл": "Файл выглядит подозрительно. Формат не соответвует действительному. Разрешенные "
                               "расширения: '%(allowed_extensions)s'.",
        "Тип не поддерживается": "Расширение файла : '%(extension)s' не разрешено. "
                                 "Разрешенные расширения: '%(allowed_extensions)s'."
    }
    code = 'invalid_extension'
    ext_cnt_mapping = {
        "png": "image/png",
        "heic": "image/heic",
        "heif": "image/heif",
        "jpeg": "image/jpeg",
        "jpg": "image/jpeg",
    }

    def __init__(self, ):
        self.allowed_extensions = [allowed_extension.lower() for
                                   allowed_extension in self.ext_cnt_mapping.keys()]

    def __call__(self, data):
        extension = Path(data.name).suffix[1:].lower()
        content_type = magic.from_buffer(data.read(1024), mime=True)
        if extension not in self.allowed_extensions:
            raise ValidationError(
                self.messages['Тип не поддерживается'],
                code=self.code,
                params={
                    'extension': extension,
                    'allowed_extensions': ', '.join(self.allowed_extensions)
                }
            )
        if content_type != self.ext_cnt_mapping[extension]:
            raise ValidationError(
                self.messages['Подозрительный файл'],
                code=self.code,
                params={
                    'allowed_extensions': ', '.join(self.allowed_extensions)
                }
            )

    def __eq__(self, other):
        return (
                isinstance(other, self.__class__) and
                self.allowed_extensions == other.allowed_extensions and
                self.message == other.message and
                self.code == other.code
        )


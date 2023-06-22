import re

from rest_framework.serializers import ModelSerializer, ValidationError


class CustomSerializer(ModelSerializer):
    """Кастомный сериализатор."""

    def validate_slug(self, value):
        """Валидация поля slug на соответствие паттерну."""
        pattern = r'^[-a-zA-Z0-9_]+$'
        if not re.match(pattern, value):
            raise ValidationError(
                'Поле slug может содержать буквы латинского алфавита в верхнем'
                'и нижнем регистре, цифры от 0-9,подчеркивание(_), дефис(-)'
            )
        return value

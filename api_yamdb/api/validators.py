from api_yamdb.settings import PATTERN
import re
from django.core.exceptions import ValidationError

from api_yamdb.settings import ROLE_TYPE


def validate_username_pattern(value):
    """Проверка username на соответствие паттерну."""
    if not re.match(PATTERN, value):
        raise ValidationError('Username не соответствует паттерну.')
    return value


def validate_username_not_me(value):
    """Проверка на создание username - me."""
    if value == 'me':
        raise ValidationError('Имя пользователя me запрещено!')
    return value


def validate_role(value):
    """Проверка допустимых ролей."""
    if value not in [role[0] for role in ROLE_TYPE]:
        raise ValidationError('Такой роли не существует.')
    return value

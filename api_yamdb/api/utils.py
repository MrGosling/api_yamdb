from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb.settings import FROM_EMAIL


def confirm_code_send_mail(username, email, confirmation_code):
    """Отправка письма с кодом подтверждения."""
    send_mail(
        'Регистрация',
        (
            f'Здравствуйте, {username}, '
            f'ваш код подтверждения: {confirmation_code}.'
        ),
        FROM_EMAIL,
        [email],
        fail_silently=False,
    )


def get_tokens_for_user(user):
    """Получение токена для авторизации."""
    refresh = RefreshToken.for_user(user)

    return {
        'token': str(refresh.access_token),
    }

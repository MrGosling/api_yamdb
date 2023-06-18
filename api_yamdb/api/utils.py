from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken


def confirm_code_send_mail(username, email, confirmation_code):
    send_mail(
        'Регистрация',
        (
            f'Здравствуйте, {username}, '
            f'ваш код подтверждения: {confirmation_code}.'
        ),
        'from@example.com',
        [email],
        fail_silently=False,
    )


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'token': str(refresh.access_token),
    }

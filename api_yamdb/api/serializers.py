from rest_framework.serializers import ModelSerializer, EmailField, CharField

from reviews.models import CustomUser


class UserSerializer(ModelSerializer):
    email = EmailField(required=True)
    username = CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class PartialUserSerializer(ModelSerializer):
    username = CharField(read_only=True)
    role = CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response

from api.serializers import UserSerializer, PartialUserSerializer
from api.permissions import AdminPermission, UserPermission
from reviews.models import CustomUser


class AdminUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AdminPermission]
    lookup_field = 'username'

    def retrieve(self, *args, **kwargs):
        user = get_object_or_404(
            self.queryset, username=self.kwargs.get('username')
        )
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserViewSet(ModelViewSet):
    serializer_class = PartialUserSerializer
    permission_classes = [UserPermission]

    def get_queryset(self):
        return CustomUser.objects.filter(username=self.request.user.username)

    def get_object(self):
        return self.request.user

    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset.first())
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = PartialUserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

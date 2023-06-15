from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from api.serializers import UserSerializer, PartialUserSerializer
from api.permissions import AdminPermission, UserPermission
from reviews.models import CustomUser


class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AdminPermission]
    lookup_field = "username"

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[UserPermission]
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = PartialUserSerializer(request.user)
            return Response(serializer.data)

        user = request.user
        serializer = PartialUserSerializer(
            user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

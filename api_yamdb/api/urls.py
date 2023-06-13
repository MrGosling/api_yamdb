from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from api.views import AdminUserViewSet, UserViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('users/me', UserViewSet, basename='users_me')
router.register('users', AdminUserViewSet, basename='users')
router.register('users/<str:username>', AdminUserViewSet, basename='users')


urlpatterns = [
    path('v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_view'),
    path('v1/', include(router.urls)),
]

from rest_framework_simplejwt.views import TokenObtainPairView
from django.urls import include, path
from rest_framework import routers
from api.views import TitleViewSet, GenreViewSet, CategoryViewSet, ReviewViewSet, CommentViewSet, UserViewSet, AuthViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('auth', AuthViewSet, basename='auth')
router.register('users', UserViewSet, basename='users')
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews',
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)

urlpatterns = [
    # path('v1/auth/signup/', ),
    path('v1/auth/token/',
         TokenObtainPairView.as_view(),
         name='token_obtain_view',
         ),
    path('v1/', include(router.urls)),
]

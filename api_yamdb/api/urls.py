from django.urls import include, path
from rest_framework import routers
from api.views import ReviewViewSet, CommentViewSet
from api.views import TitleViewSet, GenreViewSet, CategoryViewSet

app_name = 'api'

router = routers.DefaultRouter()
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
    path('v1/', include(router.urls)),
]


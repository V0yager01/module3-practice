from django.urls import path, include
from rest_framework import routers

from .views import VideoViewSet

router = routers.DefaultRouter()

router.register(
    'videos',
    VideoViewSet,
    basename='videos'
)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]

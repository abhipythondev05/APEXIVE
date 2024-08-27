# myapp/urls.py

from django.urls import path,include
from .views import uploaded_and_downloaded_view,recently_modified_view
from rest_framework.routers import DefaultRouter
from .views import ImagePicViewSet

router = DefaultRouter()
router.register(r'images', ImagePicViewSet)

urlpatterns = [
    path('uploaded-and-downloaded/', uploaded_and_downloaded_view, name='uploaded_and_downloaded'),
    path('recent-images/', recently_modified_view, name='recently_modified_view'),
     path('', include(router.urls)),
]



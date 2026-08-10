from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BorrowViewSet

router = DefaultRouter()
router.register(r"borrow", BorrowViewSet, basename="borrow")

urlpatterns = [
    path("", include(router.urls)),
]

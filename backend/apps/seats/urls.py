from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, SeatViewSet, SeatSearchView

router = DefaultRouter()
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'seats', SeatViewSet, basename='seat')

urlpatterns = [
    path('', include(router.urls)),
    path('/search/', SeatSearchView.as_view(), name='seat-search'),
]

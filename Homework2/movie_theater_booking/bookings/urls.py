from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
router = DefaultRouter()
router.register(r"movies", views.MovieViewSet, basename="movies")
router.register(r"seats", views.SeatViewSet, basename="seats")
router.register(r"bookings", views.BookingViewSet, basename="bookings")
urlpatterns = [
    path("", include(router.urls)),
]
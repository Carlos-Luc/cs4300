from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
router = DefaultRouter()
router.register(r"movies", views.MovieViewSet, basename="movies")
router.register(r"seats", views.SeatViewSet, basename="seats")
router.register(r"bookings", views.BookingViewSet, basename="bookings")
urlpatterns = [
    path("api/", include(router.urls)),
    path("", views.movie_list, name="movie_list"),
    path("book_seat/<int:movie_id>/", views.book_seat, name="book_seat"),
    path("history/", views.booking_history, name="history")
]
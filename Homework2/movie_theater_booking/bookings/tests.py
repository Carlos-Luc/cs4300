from django.test import TestCase

# Create your tests here.

"""Tests for the bookings app: API permissions, booking logic, and template views."""
from datetime import date

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Movie, Seat, Booking

User = get_user_model()


class BookingAppTestBase(APITestCase):
    """Shared test data: two normal users, one staff user, a movie, and two seats."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="alice", password="testpass123")
        cls.other_user = User.objects.create_user(username="bob", password="testpass123")
        cls.admin = User.objects.create_user(
            username="staff", password="testpass123", is_staff=True
        )
        cls.movie = Movie.objects.create(
            title="Test Movie",
            description="A test movie",
            release_date=date(2020, 1, 1),
            runtime=90,
        )
        cls.seat = Seat.objects.create(number=1)
        cls.seat2 = Seat.objects.create(number=2)

    def make_booking(self, user, seat=None):
        """Creates a booking directly in the database and marks the seat as booked."""
        seat = seat or self.seat
        booking = Booking.objects.create(movie=self.movie, seat=seat, user=user)
        seat.booking_status = True
        seat.save()
        return booking


class ModelTests(BookingAppTestBase):
    """String representations used by the admin."""

    def test_movie_str(self):
        self.assertEqual(str(self.movie), "Test Movie")

    def test_seat_str_contains_number(self):
        self.assertIn("1", str(self.seat))

    def test_new_seat_is_available(self):
        self.assertFalse(Seat.objects.create(number=3).booking_status)


class MovieAPITests(BookingAppTestBase):
    """Permission rules for /api/movies/: anyone reads, only staff writes."""

    movie_data = {
        "title": "New Movie",
        "description": "x",
        "release_date": "2021-01-01",
        "runtime": 100,
    }

    def test_anyone_can_list_movies(self):
        response = self.client.get("/api/movies/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Test Movie")

    def test_anonymous_cannot_create_movie(self):
        response = self.client.post("/api/movies/", self.movie_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_normal_user_cannot_create_movie(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/movies/", self.movie_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_normal_user_cannot_delete_movie(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/movies/{self.movie.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Movie.objects.filter(id=self.movie.id).exists())

    def test_admin_can_create_movie(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post("/api/movies/", self.movie_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), 2)

    def test_admin_can_delete_movie(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f"/api/movies/{self.movie.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class BookingAPITests(BookingAppTestBase):
    """Booking creation, double-booking prevention, privacy, and allowed methods."""

    def test_booking_sets_user_and_marks_seat(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/bookings/", {"movie": self.movie.id, "seat": self.seat.id}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.seat.refresh_from_db()
        self.assertTrue(self.seat.booking_status)
        self.assertEqual(Booking.objects.get().user, self.user)

    def test_client_cannot_set_booking_user(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(
            "/api/bookings/",
            {"movie": self.movie.id, "seat": self.seat.id, "user": self.other_user.id},
        )
        self.assertEqual(Booking.objects.get().user, self.user)

    def test_double_booking_rejected(self):
        self.client.force_authenticate(user=self.user)
        data = {"movie": self.movie.id, "seat": self.seat.id}
        self.client.post("/api/bookings/", data)
        response = self.client.post("/api/bookings/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("seat", response.data)
        self.assertEqual(Booking.objects.count(), 1)

    def test_invalid_movie_rejected(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/bookings/", {"movie": 999, "seat": self.seat.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_anonymous_cannot_view_bookings(self):
        response = self.client.get("/api/bookings/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_cannot_create_booking(self):
        response = self.client.post(
            "/api/bookings/", {"movie": self.movie.id, "seat": self.seat.id}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Booking.objects.count(), 0)

    def test_user_only_lists_own_bookings(self):
        self.make_booking(self.user, self.seat)
        self.make_booking(self.other_user, self.seat2)
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/bookings/")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["user"], self.user.id)

    def test_user_cannot_see_others_booking(self):
        booking = self.make_booking(self.other_user)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/bookings/{booking.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_owner_can_see_own_booking(self):
        booking = self.make_booking(self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/bookings/{booking.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_booking_cannot_be_deleted(self):
        booking = self.make_booking(self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/bookings/{booking.id}/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_booking_cannot_be_edited(self):
        booking = self.make_booking(self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f"/api/bookings/{booking.id}/", {"seat": self.seat2.id})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class SeatAPITests(BookingAppTestBase):
    """Availability filtering and the /api/seats/<id>/booking/ action."""

    def booking_url(self, seat):
        return f"/api/seats/{seat.id}/booking/"

    def test_booked_seat_hidden_from_list(self):
        self.seat.booking_status = True
        self.seat.save()
        response = self.client.get("/api/seats/")
        ids = [s["id"] for s in response.data]
        self.assertNotIn(self.seat.id, ids)
        self.assertIn(self.seat2.id, ids)

    def test_seats_are_read_only(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post("/api/seats/", {"number": 50})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_seat_booking_action(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.booking_url(self.seat), {"movie": self.movie.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.seat.refresh_from_db()
        self.assertTrue(self.seat.booking_status)
        self.assertEqual(Booking.objects.get().user, self.user)

    def test_seat_booking_action_requires_login(self):
        response = self.client.post(self.booking_url(self.seat), {"movie": self.movie.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_seat_booking_action_requires_movie(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.booking_url(self.seat), {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_seat_booking_action_rejects_booked_seat(self):
        self.make_booking(self.other_user)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.booking_url(self.seat), {"movie": self.movie.id})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_seat_booking_action_rejects_get(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.booking_url(self.seat))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class TemplateViewTests(BookingAppTestBase):
    """The HTML pages: movie list, seat booking, and booking history."""

    HISTORY_URL_NAME = "history" 

    def test_movie_list_shows_movies(self):
        response = self.client.get(reverse("movie_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Movie")

    def test_book_seat_requires_login(self):
        url = reverse("book_seat", args=[self.movie.id])
        response = self.client.get(url)
        login_url = reverse("rest_framework:login")
        self.assertRedirects(
            response, f"{login_url}?next={url}", fetch_redirect_response=False
        )

    def test_book_seat_shows_only_available_seats(self):
        self.make_booking(self.other_user, self.seat)
        self.client.force_login(self.user)
        response = self.client.get(reverse("book_seat", args=[self.movie.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["available_seats"]), [self.seat2])

    def test_book_seat_invalid_movie_404(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("book_seat", args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_book_seat_form_creates_booking(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("book_seat", args=[self.movie.id]), {"seat_selection": self.seat.id}
        )
        self.assertRedirects(response, reverse("history"))
        self.assertEqual(Booking.objects.get().user, self.user)
        self.seat.refresh_from_db()
        self.assertTrue(self.seat.booking_status)

    def test_book_seat_form_rejects_booked_seat(self):
        self.make_booking(self.other_user, self.seat)
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("book_seat", args=[self.movie.id]), {"seat_selection": self.seat.id}
        )
        self.assertEqual(response.status_code, 200)  # page re-rendered, no redirect
        self.assertEqual(Booking.objects.count(), 1)

    def test_book_seat_form_without_seat(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("book_seat", args=[self.movie.id]), {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Booking.objects.count(), 0)

    def test_history_requires_login(self):
        response = self.client.get(reverse(self.HISTORY_URL_NAME))
        self.assertEqual(response.status_code, 302)

    def test_history_shows_only_own_bookings(self):
        self.make_booking(self.user, self.seat)
        self.make_booking(self.other_user, self.seat2)
        self.client.force_login(self.user)
        response = self.client.get(reverse(self.HISTORY_URL_NAME))
        self.assertEqual(response.status_code, 200)
        bookings = list(response.context["bookings"])
        self.assertEqual(len(bookings), 1)
        self.assertEqual(bookings[0].user, self.user)
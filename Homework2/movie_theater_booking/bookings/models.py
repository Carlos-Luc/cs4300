from django.db import models
from django.conf import settings

class Movie(models.Model):
    '''Movie model: Info about a movie like its title, description, release date and run time in minutes'''
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    runtime = models.PositiveIntegerField()

    def __str__(self):

        return self.title

class Seat(models.Model):
    '''Seat model: Info about a seat such as its number and the status of its booking'''
    number = models.PositiveIntegerField(unique=True)
    booking_status = models.BooleanField(default=False)

    def __str__(self):

        return f"Seat: {self.number}"


class Booking(models.Model):
    '''Booking model: Info about a booking such as which movie, which seat, which user and when the booking is'''
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.user}: {self.movie}, {self.date}, {self.seat}"
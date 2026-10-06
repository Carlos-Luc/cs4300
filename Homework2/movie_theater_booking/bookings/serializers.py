from rest_framework import serializers
from .models import Movie, Seat, Booking

class MovieSerializer(serializers.ModelSerializer):
    '''Serializes a Movie model instance'''
    class Meta:
        model = Movie
        fields = ["id", "title", "description", "release_date", "runtime"]

class SeatSerializer(serializers.ModelSerializer):
    '''Serializes a Seat model instance'''
    class Meta:
        model = Seat
        fields = ["id", "number", "booking_status"]
        read_only_fields = ["booking_status"]

class BookingSerializer(serializers.ModelSerializer):
    '''Serializes a Booking model instance. Also makes user and date field read only'''
    class Meta:
        model = Booking
        fields = ["id", "movie", "seat", "user", "date"]
        read_only_fields = ["user", "date"]
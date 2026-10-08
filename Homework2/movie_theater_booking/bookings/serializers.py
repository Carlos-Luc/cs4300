from rest_framework import serializers
from django.contrib.auth.models import User
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
    
    def validate_seat(self, value):
        #Checks if seat has been booked
        if not value.booking_status:
        
            return value
        #Raises Error when seat is booked
        else:
             raise serializers.ValidationError("This seat is already booked")
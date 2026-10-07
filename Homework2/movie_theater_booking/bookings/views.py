from django.shortcuts import render
from rest_framework import viewsets, permissions , mixins
from rest_framework import serializers
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer
from .models import Movie, Seat, Booking


class MovieViewSet(viewsets.ModelViewSet):
    '''View set provides CRUD operations on movies'''
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAdminUser]

class SeatViewSet(viewsets.ReadOnlyModelViewSet):
    '''Seat Viewset: give list of all avilable seats'''
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

    def get_queryset(self):

        return Seat.objects.filter(booking_status = False)
#Custom viewset to only only allow creation, retrevial and listing. Deleting and editing bookings are not available.
class BookingViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    Booking Viewset: Only usable by Authenticated users, bookings are only visable to user who created it, when bookings are
    created seating booking status is changed, Double bookings are prevented
    '''
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    #Overrides get_queryset so that it filters bookings by associated user and returns that list
    def get_queryset(self):

        this_user = self.request.user
        return Booking.objects.filter(user=this_user)
    #Associates Users with bookings
    def perform_create(self, serializer):
        seat = serializer.validated_data.get('seat')
        #Checks if seat is booked then saves a booking for that user and changes seat booking_status to true
        if not seat.booking_status:
        
            serializer.save(user=self.request.user)

            seat.booking_status = True

            seat.save()
        #Raises Error when seat is booked
        else:
             raise serializers.ValidationError("This seat is already booked")
    
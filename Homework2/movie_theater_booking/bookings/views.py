from django.shortcuts import render
from rest_framework import viewsets, permissions , mixins
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from .permissions import IsAdminOrReadOnly
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer
from .models import Movie, Seat, Booking


class MovieViewSet(viewsets.ModelViewSet):
    '''View set provides CRUD operations on movies. Ops only available to admins'''
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAdminOrReadOnly]

class SeatViewSet(viewsets.ReadOnlyModelViewSet):
    '''Seat Viewset: give list of all avilable seats'''
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

    def get_queryset(self):

        return Seat.objects.filter(booking_status=False)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def booking(self, request, *args, **kwargs):
        '''Books seat for logged in user that is available, must include movie id in the post'''
        seat = self.get_object()
        movie = request.data.get('movie')
        serializer = BookingSerializer(data={"seat": seat.id, "movie": movie})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        seat.booking_status = True
        seat.save()
        return Response(serializer.data, status=201)


#Custom viewset to only only allow creation, retrevial and listing. Deleting and editing bookings are not available.
class BookingViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    Booking Viewset: Only usable by Authenticated users, bookings are only visable to user who created it, when bookings are
    created seating booking status is changed, Double bookings are prevented
    '''
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

   
    def get_queryset(self):
        '''Overrides get_queryset so that it filters bookings by associated user and returns that list'''
        this_user = self.request.user
        return Booking.objects.filter(user=this_user)

    def perform_create(self, serializer):
        '''Saves the booking for the logged-in user and marks the seat as booked.'''
        seat = serializer.validated_data.get('seat')
        serializer.save(user=self.request.user)
        seat.booking_status = True
        seat.save()
    
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions , mixins
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from .permissions import IsAdminOrReadOnly
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer
from .models import Movie, Seat, Booking

def movie_list(request):
    '''Shows List of available movies'''
    movies = Movie.objects.all()
    return render(request, "bookings/movie_list.html",{"movies":movies})

@login_required
def book_seat(request, movie_id):
    '''Allows viewing and booking of available seat for a movie, if logged out redirected to DRF login page'''
    movies = get_object_or_404(Movie, pk=movie_id)
    available_seats = Seat.objects.filter(booking_status=False)
    #Gets available seats for movie
    if(request.method == "GET"):
        return render(request, "bookings/seat_booking.html",{"movies":movies, "available_seats": available_seats})
    #Posts a created Booking using selected seat
    elif(request.method == "POST"):
        seat_id = request.POST.get("seat_selection")
        serializer = BookingSerializer(data={"seat": seat_id, "movie": movie_id})
        if(serializer.is_valid()):
            seat = serializer.validated_data.get("seat")
            serializer.save(user=request.user)
            seat.booking_status = True
            seat.save()
            return redirect("history")
        else:
            return render(request, "bookings/seat_booking.html",{"movies":movies, "available_seats": available_seats})

@login_required
def booking_history(request):
    '''Shows current user's booking history, must be logged in to view'''
    bookings = Booking.objects.filter(user=request.user).order_by('-date')
    return render(request, "bookings/booking_history.html",{"bookings":bookings})
    

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
    
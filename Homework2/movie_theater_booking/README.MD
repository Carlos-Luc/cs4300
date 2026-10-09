# Render Link
https://movie-theater-booking-ljya.onrender.com
# How To Run My Django Project Locally

1. 
Run 
```bash 
cd cs4300/Homework2/movie_theater_booking         
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
```
Use the super user to use admin functions
# How to Run My Django Project Tests

1. Follow step 1 from above up until running the server
2. Run 
```bash
python3 manage.py test bookings 
```

# API Endpoints

* api/movies : Lists all movies but only allows CRUD Operations by Admins
* api/bookings : List all of current users bookings and allows for creation of bookings if logged in
* api/seats : List all available seats
* api/seats/seat.id/booking : Special action to allow you to make a booking with an available seat, must be logged in. In POST body add {"movie": movie.id} to successfully make a booking with the seat

# AI Disclaimer

Anthropic's Claude was used in the creation of this project. Claude was mainly used for guidance, summation of documentation for Django, DRF, and bootstrap, and debugging. Only generated Claude code used was for testing suite.


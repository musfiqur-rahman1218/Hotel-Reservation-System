from django.urls import path
from .views import HotelListView, ReservationCreateView

urlpatterns = [
    path('hotels/', HotelListView.as_view(), name='hotel-list'),
    path('reservations/', ReservationCreateView.as_view(), name='reservation-create'),
]

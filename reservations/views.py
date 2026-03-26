from rest_framework import generics, status
from rest_framework.response import Response
from .models import Hotel, Reservation
from .serializers import HotelSerializer, ReservationSerializer
from datetime import datetime
from django.db.models import Count, Q, F

class HotelListView(generics.ListAPIView):
    serializer_class = HotelSerializer

    def get_queryset(self):
        checkin_str = self.request.query_params.get('checkin')
        checkout_str = self.request.query_params.get('checkout')

        if not checkin_str or not checkout_str:
            return Hotel.objects.none()

        try:
            checkin = datetime.strptime(checkin_str, '%Y-%m-%d').date()
            checkout = datetime.strptime(checkout_str, '%Y-%m-%d').date()
            if checkin >= checkout:
                return Hotel.objects.none()
        except ValueError:
            return Hotel.objects.none()

        # overlapping: existing checkin < search checkout AND existing checkout > search checkin
        overlapping = Q(reservations__checkin__lt=checkout, reservations__checkout__gt=checkin)
        
        hotels = Hotel.objects.annotate(
            booked_rooms=Count('reservations', filter=overlapping)
        ).filter(total_rooms__gt=F('booked_rooms'))

        return hotels

    def list(self, request, *args, **kwargs):
        checkin_str = self.request.query_params.get('checkin')
        checkout_str = self.request.query_params.get('checkout')
        
        if not checkin_str or not checkout_str:
            return Response(
                {"error": "checkin and checkout dates are required query parameters."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            checkin = datetime.strptime(checkin_str, '%Y-%m-%d').date()
            checkout = datetime.strptime(checkout_str, '%Y-%m-%d').date()
            if checkin >= checkout:
                return Response(
                    {"error": "checkin date cannot be after or equal to checkout date."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().list(request, *args, **kwargs)

class ReservationCreateView(generics.CreateAPIView):
    serializer_class = ReservationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        reservation = serializer.instance
        return Response(
            {"confirmation_number": reservation.confirmation_number},
            status=status.HTTP_201_CREATED
        )

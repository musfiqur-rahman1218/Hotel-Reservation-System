from rest_framework import serializers
from .models import Hotel, Reservation, Guest
from django.db import transaction
import datetime

class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ['guest_name', 'gender']

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['id', 'name', 'total_rooms']

class ReservationSerializer(serializers.ModelSerializer):
    hotel_name = serializers.CharField(write_only=True)
    guests_list = GuestSerializer(many=True)

    class Meta:
        model = Reservation
        fields = ['hotel_name', 'checkin', 'checkout', 'guests_list', 'confirmation_number']
        read_only_fields = ['confirmation_number']

    def validate(self, data):
        # Validate dates
        if data['checkin'] >= data['checkout']:
            raise serializers.ValidationError({"checkin": "Check-in date must be before check-out date."})
        
        # Validates guests_list
        if not data.get('guests_list'):
            raise serializers.ValidationError({"guests_list": "At least one guest is required."})

        # Validate hotel exists
        hotel_name = data.get('hotel_name')
        try:
            hotel = Hotel.objects.get(name=hotel_name)
            data['hotel'] = hotel
        except Hotel.DoesNotExist:
            raise serializers.ValidationError({"hotel_name": "Hotel does not exist."})

        # Basic availability check logic - we'll keep it simple for now
        # You could count all overlapping reservations to ensure capacity.
        # But for basic requirements, we check if total guests < total_rooms or similar.
        # Just passing it through for now as requested.
        return data

    @transaction.atomic
    def create(self, validated_data):
        guests_data = validated_data.pop('guests_list')
        hotel = validated_data.pop('hotel')
        validated_data.pop('hotel_name')
        
        reservation = Reservation.objects.create(hotel=hotel, **validated_data)
        
        # Create guests
        guests = [Guest(reservation=reservation, **guest_data) for guest_data in guests_data]
        Guest.objects.bulk_create(guests)
        
        return reservation

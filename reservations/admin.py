from django.contrib import admin
from .models import Hotel, Reservation, Guest

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_rooms')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('confirmation_number', 'hotel', 'checkin', 'checkout')
    search_fields = ('confirmation_number', 'hotel__name')

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('guest_name', 'reservation', 'gender')
    search_fields = ('guest_name',)

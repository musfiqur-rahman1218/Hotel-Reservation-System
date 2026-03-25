from django.db import models
import uuid

class Hotel(models.Model):
    name = models.CharField(max_length=255)
    total_rooms = models.PositiveIntegerField(default=10)

    def __str__(self):
        return self.name

class Reservation(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reservations')
    checkin = models.DateField()
    checkout = models.DateField()
    confirmation_number = models.CharField(max_length=100, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.confirmation_number:
            self.confirmation_number = str(uuid.uuid4()).replace('-', '')[:10].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Res {self.confirmation_number} at {self.hotel.name}"

class Guest(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='guests_list')
    guest_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.guest_name

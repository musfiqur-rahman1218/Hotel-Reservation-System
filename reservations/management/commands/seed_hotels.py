from django.core.management.base import BaseCommand
from reservations.models import Hotel

class Command(BaseCommand):
    help = 'Seeds the database with initial hotel data'

    def handle(self, *args, **kwargs):
        hotels = [
            {'name': 'The Grand Plaza', 'total_rooms': 50},
            {'name': 'Ocean View Resort', 'total_rooms': 30},
            {'name': 'Mountain Retreat', 'total_rooms': 20},
            {'name': 'City Central Inn', 'total_rooms': 100},
        ]
        
        for hotel_data in hotels:
            hotel, created = Hotel.objects.get_or_create(
                name=hotel_data['name'], 
                defaults={'total_rooms': hotel_data['total_rooms']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created {hotel.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"{hotel.name} already exists"))

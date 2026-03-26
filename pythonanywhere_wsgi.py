# This is the exact WSGI snippet you should paste into your PythonAnywhere WSGI configuration file.
# You can find the link to your WSGI configuration file on the 'Web' tab in PythonAnywhere.

import os
import sys

# Assuming your project is cloned directly into your home directory:
path = '/home/musfiqur/Hotel-Reservation-System'
if path not in sys.path:
    sys.path.insert(0, path)

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'hotel_reservation.settings'

# Load environment variables from .env (PythonAnywhere specific)
from dotenv import load_dotenv
project_folder = os.path.expanduser('~/Hotel-Reservation-System')
load_dotenv(os.path.join(project_folder, '.env'))

# Important: serve the application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

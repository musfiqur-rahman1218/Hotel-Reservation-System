#!/bin/bash
set -e

echo "Starting automated deployment script..."

# Ensure we are in the right directory
cd /home/musfiqur/Hotel-Reservation-System

# Create virtualenv if it doesn't exist
source virtualenvwrapper.sh
if [ ! -d "/home/musfiqur/.virtualenvs/hotel-env" ]; then
    mkvirtualenv --python=/usr/bin/python3.10 hotel-env
else
    workon hotel-env
fi

# Install requirements
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
sed -i 's/SECRET_KEY=.*/SECRET_KEY=django-insecure-my-random-key-for-pythonanywhere/' .env
sed -i 's/DEBUG=.*/DEBUG=False/' .env
sed -i 's/ALLOWED_HOSTS=.*/ALLOWED_HOSTS=musfiqur.pythonanywhere.com/' .env

# Clear existing db config and explicitly force sqlite3 for this deployment to avoid PA MySQL credential prompting
sed -i '/DATABASE_URL=/d' .env
echo "" >> .env
echo "DATABASE_URL=sqlite:///db.sqlite3" >> .env

# Run migrations
python manage.py migrate

# Create admin superuser
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')" || true

# Collect Static Files
python manage.py collectstatic --noinput

echo "Deployment script completed cleanly!"

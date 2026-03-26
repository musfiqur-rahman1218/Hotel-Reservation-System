# Hotel Reservation System REST API

A Django REST Framework backend for a Hotel Reservation System. Built with Python 3, Django, DRF, and MySQL. Ready for future AWS Elastic Beanstalk deployment.

## Prerequisites
- Python 3.12+ 
- `uv` package manager
- MySQL (configured to `root` with password `roo`, database `hotel`)

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/musfiqur-rahman1218/Hotel-Reservation-System.git
   cd Hotel-Reservation-System
   ```

2. **Setup virtual environment with uv**
   ```bash
   uv venv
   .\.venv\Scripts\activate
   uv pip install -r requirements.txt
   ```

3. **Configure Database (MySQL)**
   Ensure your MySQL server is running. Create the database:
   ```sql
   CREATE DATABASE IF NOT EXISTS hotel;
   ```
   The application connects to `mysql://root:roo@localhost:3306/hotel` by default. You can override this using a `.env` file (see `.env.example`).

4. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create Superuser and Seed Data**
   ```bash
   python manage.py createsuperuser
   python manage.py seed_hotels
   ```

6. **Run Server**
   ```bash
   python manage.py runserver
   ```

## API Documentation

Interactive Swagger API docs are available at:
`GET http://127.0.0.1:8000/api/schema/swagger-ui/`

### 1. Get List of Available Hotels
- **Method:** `GET`
- **Endpoint:** `/api/hotels/`
- **Query Parameters:** `checkin` (YYYY-MM-DD), `checkout` (YYYY-MM-DD)
- **Response:**
  ```json
  [
      {
          "id": 1,
          "name": "The Grand Plaza",
          "total_rooms": 50
      }
  ]
  ```

### 2. Confirm a Reservation
- **Method:** `POST`
- **Endpoint:** `/api/reservations/`
- **Body:**
  ```json
  {
    "hotel_name": "The Grand Plaza",
    "checkin": "2026-05-01",
    "checkout": "2026-05-05",
    "guests_list": [
      {
        "guest_name": "John Doe",
        "gender": "Male"
      }
    ]
  }
  ```
- **Response:**
  ```json
  {
    "confirmation_number": "A1B2C3D4E5"
  }
  ```

## AWS Elastic Beanstalk Readiness
This application is configured for easy deployment to AWS Elastic Beanstalk:
- Uses `dj-database-url` to handle DB connection strings dynamically.
- Includes `gunicorn` in `requirements.txt`.
- Includes `whitenoise` for robust static file serving.
- Secrets and configurations are loaded from environment variables (`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`).

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

## How to Run the Project

Once the database is set up and migrations are applied, follow these steps to run the REST API locally:

1. Ensure your virtual environment is active:
   ```bash
   .\.venv\Scripts\activate
   ```

2. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

3. The server will start on `http://127.0.0.1:8000/`.
4. You can explore the interactive API schema (Swagger UI) by navigating to `http://127.0.0.1:8000/api/schema/swagger-ui/` in your browser.

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

## PythonAnywhere Step-by-Step Deployment Guide

Follow these exact instructions to deploy to your PythonAnywhere account (`musfiqur`). 

### 1. Open a Bash Console
Log in to PythonAnywhere. Go to your Dashboard, click **Consoles**, and start a new **Bash** console.

### 2. Clone the Repository
In the Bash console, run:
```bash
git clone https://github.com/musfiqur-rahman1218/Hotel-Reservation-System.git
cd Hotel-Reservation-System
```

### 3. Create Virtual Environment
PythonAnywhere has virtualenv pre-installed. Run:
```bash
mkvirtualenv --python=/usr/bin/python3.10 hotel-env
```
*(If you are prompted, use the python version provided by your PythonAnywhere plan)*

### 4. Install Requirements
With the virtual environment active, run:
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Copy the `.env.example` file and safely add your secrets:
```bash
cp .env.example .env
nano .env
```
Ensure you set:
- `SECRET_KEY="..."`
- `DEBUG=False`
- `ALLOWED_HOSTS=musfiqur.pythonanywhere.com`
- `DATABASE_URL=mysql://musfiqur:<YOUR_PA_DB_PASSWORD>@musfiqur.mysql.pythonanywhere-services.com/musfiqur$hotel` (or use the SQLite URL if you're avoiding external database configuration).

Save and exit nano (`Ctrl+O`, `Enter`, `Ctrl+X`).

### 6. Run Migrations
Apply your database schema:
```bash
python manage.py migrate
```

### 7. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 8. Collect Static Files
Gather all static files so WhiteNoise can serve them:
```bash
python manage.py collectstatic --noinput
```

### 9. Configure the Web App
1. Go to your PythonAnywhere **Web** tab.
2. Click **Add a new web app**.
3. Choose **Manual configuration** (do NOT choose Django).
4. Select Python version (e.g., 3.10) to match your virtualenv.
5. In the **Virtualenv** section, enter the path: `/home/musfiqur/.virtualenvs/hotel-env`
6. In the **Source code** section, enter: `/home/musfiqur/Hotel-Reservation-System`

### 10. Edit WSGI File
1. On the **Web** tab, click the link to your **WSGI configuration file** (e.g., `/var/www/musfiqur_pythonanywhere_com_wsgi.py`).
2. Delete everything inside it.
3. Open `pythonanywhere_wsgi.py` from the project repository and copy its entire contents.
4. Paste it into the PythonAnywhere WSGI file and **Save**.

### 11. Reload the Web App
Go back to the **Web** tab and click the big green **Reload musfiqur.pythonanywhere.com** button.


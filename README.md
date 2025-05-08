# Library Management System

A Django REST Framework application for managing a digital library, including books, authors, publishers, and user reviews.

## Technologies

- Django 5.0+
- Django REST Framework
- PostgreSQL 15+
- Docker & Docker Compose
- Gunicorn WSGI server

## Installation & Setup

### Local Development

1. Clone the repository
```bash
git clone <repository-url>
cd AIEMS
```

2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run migrations
```bash
python manage.py migrate
```

5. Start the development server
```bash
python manage.py runserver
```

### Docker Deployment

1. Build and run with Docker Compose
```bash
docker-compose build
docker-compose up --detach
```

2. Access the application at `http://localhost:8000/`

## Documentation

- **API Demo PDF**: Screenshots of all API operations are included in the `API Demo.pdf` file
- **Postman Collection**: A complete Postman collection with all API requests is provided in the repository

## Project Structure

```
Root/
├── config/              # Django project settings
├── lms/                 # Main application
│   ├── models.py        # Data models
│   ├── serializers.py   # DRF serializers
│   ├── views.py         # API views
│   └── urls.py          # API routes
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose services
└── requirements.txt     # Python dependencies
```


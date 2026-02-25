# Task Manager API

A production-ready RESTful API for managing tasks, built with **Django REST Framework**. Features JWT authentication, role-based access control, Swagger/ReDoc documentation, pagination, filtering, and comprehensive test coverage.

---

## Features

- **JWT Authentication** — Secure, stateless auth with access/refresh tokens and token blacklisting on logout
- **User Roles** — `admin` (full access to all tasks) and `user` (own tasks only)
- **Full CRUD** — Create, read, update, and delete tasks
- **Pagination** — Configurable page size via query params
- **Filtering & Search** — Filter options
- **Ordering** — Sort by any field ascending or descending
- **Swagger + ReDoc** — Interactive API documentation at `/swagger/` and `/docs/ReDoc/`
- **Unit Tests** — Full coverage of models, auth, and task endpoints

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Django 4.2 + DRF 3.14 |
| Auth | djangorestframework-simplejwt |
| Docs | drf-yasg (Swagger) + drf-spectacular (ReDoc) |
| Filtering | django-filter |
| Testing | pytest + pytest-django |
| Database | SQLite (dev) |

---

## Quick Start

### Prerequisites

- Python 3.10+
- pip

### 1. Clone & set up the environment

```bash
git clone https://github.com/saxenak569/task-manager-project.git
cd task-manager-api

python -m venv venv
source venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment variables

```bash
cp .env.example .env
# Edit .env and set a strong SECRET_KEY
```

### 3. Apply migrations

```bash
python manage.py migrate
```

### 4. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

### 5. Run the development server

```bash
python manage.py runserver
```

The API is now available at `http://127.0.0.1:8000/`.

---

## Running Tests

```bash
# Run all tests
python manage.py pytest
```

## API Documentation

| URL | Description |
|---|---|
| `/swagger/` | Swagger UI (interactive) |
| `/redoc/` | ReDoc (readable) |
| `/swagger.json` | OpenAPI JSON schema |
| `/admin/` | Django admin panel |

---

## API Reference

### Authentication Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/auth/register/` | ❌ | Register a new user |
| POST | `/api/auth/login/` | ❌ | Obtain JWT tokens |
| POST | `/api/auth/token/refresh/` | ❌ | Refresh access token |
| POST | `/api/auth/logout/` | ✅ | Blacklist refresh token |
| GET/PATCH | `/api/auth/profile/` | ✅ | View/update own profile |

### Task Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/tasks/` | ✅ | List tasks (own; admin sees all) |
| POST | `/api/tasks/` | ✅ | Create a new task |
| GET | `/api/tasks/{id}/` | ✅ | Retrieve a specific task |
| PUT | `/api/tasks/{id}/` | ✅ | Fully update a task |
| PATCH | `/api/tasks/{id}/` | ✅ | Partially update a task |
| DELETE | `/api/tasks/{id}/` | ✅ | Delete a task |

---

## Example Requests & Responses

### Register

```http
POST /api/auth/register/
Content-Type: application/json

{
  "email": "shiv@example.com",
  "username": "shiv",
  "password": "shiv123",
  "password_confirm": "shiv123"
}
```

**Response 201:**
```json
{
  "message": "User registered successfully.",
  "user": {
    "id": 1,
    "email": "shiv@example.com",
    "username": "shiv",
    "role": "user",
    "date_joined": "2026-02-25T10:00:00Z",
    "is_active": true
  }
}
```

---

### Login

```http
POST /api/auth/login/
Content-Type: application/json

{
  "email": "shiv@example.com",
  "password": "shiv123"
}
```

**Response 200:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIs...",
  "refresh": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": 1,
    "email": "shiv@example.com",
    "username": "shiv",
    "role": "user"
  }
}
```

---

### Create a Task

```http
POST /api/tasks/
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, and bread",
  "completed": false
}
```

**Response 201:**
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, and bread",
  "completed": false,
  "created_at": "2024-01-15T10:05:00Z",
  "updated_at": "2024-01-15T10:05:00Z"
}
```

---

### List Tasks with Filtering & Pagination

```http
GET /api/tasks/?completed=false&search=grocery&ordering=-created_at&page=1&page_size=5
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

**Response 200:**
```json
{
  "count": 12,
  "next": "http://localhost:8000/api/tasks/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "Milk, eggs, and bread",
      "completed": false,
      "owner": 1,
      "owner_email": "shiv@example.com",
      "created_at": "2024-01-15T10:05:00Z",
      "updated_at": "2024-01-15T10:05:00Z"
    }
  ]
}
```

---

### Partially Update a Task

```http
PATCH /api/tasks/1/
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "completed": true
}
```

**Response 200:**
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, and bread",
  "completed": true,
  "created_at": "2024-01-15T10:05:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

---

### Refresh Token

```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Response 200:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIs..."
}
```

---

## Project Structure

```
task_manager_project/
├── task_manager_project/                    # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── asgi.py
├── tasks/               
│   ├── models.py          
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py 
│   └── admin.py
├── manage.py
├── requirements.txt
└── README.md
```

---

## User Roles

| Capability | Regular User | Admin |
|---|---|---|
| View own tasks | ✅ | ✅ |
| Create tasks | ✅ | ✅ |
| Update/delete own tasks | ✅ | ✅ |
| View all users' tasks | ❌ | ✅ |
| Update/delete any task | ❌ | ✅ |

To create an admin user:
```bash
# Via Django shell
python manage.py shell -c "
from users.models import User
User.objects.create_user(
    email='admin@example.com',
    username='admin',
    password='Admin123',
    role='admin',
    is_staff=True
)
"
```

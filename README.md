# Task Manager API

A RESTful API for managing tasks, built with **Django REST Framework**. Features session-based authentication, role-based access control, filtering, and test coverage.

---

## Features

- **Session Authentication** — Secure, cookie-based auth using Django's built-in session framework
- **User Roles** — `admin` (full access to all tasks) and `basic_user` (own tasks only)
- **Full CRUD** — Create, read, update, and delete tasks
- **Filtering** — Filter tasks by `completed` status
- **Unit Tests** — Coverage of auth and task endpoints

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Django + DRF |
| Auth | Django Session Authentication |
| Filtering | django-filter |
| Testing | Django TestCase + DRF APITestCase |
| Database | SQLite (dev) |

---

## Quick Start

### Prerequisites

- Python 3.10+
- pip

### 1. Clone & set up the environment

```bash
git clone https://github.com/saxenak569/task-manager-project.git
cd task-manager-project

python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

pip install -r requirements.txt
```

### 2. Apply migrations

```bash
python manage.py migrate
```

### 3. Create a superuser (admin)

```bash
python manage.py createsuperuser
```

### 4. Run the development server

```bash
python manage.py runserver
```

The API is now available at `http://127.0.0.1:8000/`.

---

## Running Tests

```bash
python manage.py test
```

---

## API Reference

### Authentication Endpoints

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| POST | `/api/register/` | ❌ | Register a new user |
| POST | `/api/login/` | ❌ | Login and start a session |
| POST | `/api/logout/` | ✅ | Logout and clear the session |

### Task Endpoints

| Method | Endpoint | Auth Required | Description |
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
POST /api/register/
Content-Type: application/json

{
  "username": "shiv",
  "password": "shiv123",
  "role": "basic_user"
}
```

**Response 201:**
```json
{
  "id": 1,
  "username": "shiv"
}
```

> **Note:** Registering with `"role": "admin"` only grants admin privileges if the request is made by an existing admin (staff) user. Otherwise, the user is created as a `basic_user`.

---

### Login

```http
POST /api/login/
Content-Type: application/json

{
  "username": "shiv",
  "password": "shiv123"
}
```

**Response 200:**
```json
{
  "message": "Logged in successfully.",
  "user": {
    "id": 1,
    "username": "shiv",
    "is_admin": false
  }
}
```

> A session cookie (`sessionid`) is set automatically. Include it in all subsequent requests.

---

### Logout

```http
POST /api/logout/
```

**Response 200:**
```json
{
  "message": "Logged out successfully."
}
```

---

### Create a Task

```http
POST /api/tasks/
Content-Type: application/json
Cookie: sessionid=<your-session-cookie>

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
  "user": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, and bread",
  "completed": false,
  "created_at": "2026-02-26T10:05:00Z",
  "updated_at": "2026-02-26T10:05:00Z"
}
```

---

### List Tasks with Filtering

```http
GET /api/tasks/?completed=false
Cookie: sessionid=<your-session-cookie>
```

**Response 200:**
```json
[
  {
    "id": 1,
    "user": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, and bread",
    "completed": false,
    "created_at": "2026-02-26T10:05:00Z",
    "updated_at": "2026-02-26T10:05:00Z"
  }
]
```

---

### Partially Update a Task

```http
PATCH /api/tasks/1/
Content-Type: application/json
Cookie: sessionid=<your-session-cookie>

{
  "completed": true
}
```

**Response 200:**
```json
{
  "id": 1,
  "user": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, and bread",
  "completed": true,
  "created_at": "2026-02-26T10:05:00Z",
  "updated_at": "2026-02-26T10:30:00Z"
}
```

---

## Project Structure

```
task_manager_project/
├── task_manager_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tasks/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   └── admin.py
├── manage.py
└── requirements.txt
```

---

## User Roles

| Capability | Basic User | Admin |
|---|---|---|
| View own tasks | ✅ | ✅ |
| Create tasks | ✅ | ✅ |
| Update/delete own tasks | ✅ | ✅ |
| View all users' tasks | ❌ | ✅ |
| Update/delete any task | ❌ | ✅ |

To create an admin user via the shell:

```bash
python manage.py shell -c "
from django.contrib.auth.models import User
u = User.objects.create_user(username='admin', password='Admin123')
u.is_staff = True
u.save()
"
```

Or simply use:

```bash
python manage.py createsuperuser
```

---

## Settings

Ensure the following are configured in `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

`django.contrib.sessions` must be in `INSTALLED_APPS` and `SessionMiddleware` in `MIDDLEWARE` (both are included by default in a standard Django project).
# Student Management API

A small REST API for creating, reading, updating, and deleting student records. It is built with FastAPI, SQLAlchemy, and MySQL.

## Features

- Create, list, retrieve, replace, partially update, and delete students.
- Request validation for required text fields and non-negative ages.
- Consistent response models and `404 Not Found` responses for missing students.
- Database sessions are scoped to requests and failed write transactions are rolled back.
- Database configuration is loaded from environment variables.
- Interactive API documentation via Swagger UI.

## Technology stack

- Python 3.10+
- FastAPI
- SQLAlchemy
- MySQL with PyMySQL
- python-dotenv
- Uvicorn

## Project structure

```text
student-management-api/
├── routers/
│   ├── __init__.py
│   └── students.py
├── database.py
├── main.py
├── models.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.10 or newer
- A running MySQL server
- A MySQL database (for example, `fastapi_db`)

## Installation

Clone the repository, then create and activate a virtual environment.

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

On macOS or Linux, activate it with `source venv/bin/activate`.

## Environment configuration

Copy the example file and update it with your local database credentials.

```powershell
Copy-Item .env.example .env
```

Set `DATABASE_URL` in `.env`:

```env
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/fastapi_db
```

If the user name or password contains URL-reserved characters such as `@`, URL-encode them. `.env` is deliberately ignored by Git; never commit database credentials.

## Database setup

Create the database in MySQL if it does not already exist:

```sql
CREATE DATABASE fastapi_db;
```

The API creates the `students` table on application startup. The configured MySQL user must be able to create and modify tables in this database.

## Run the server

```powershell
uvicorn main:app --reload
```

Open Swagger UI at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). The OpenAPI schema is available at `/openapi.json`.

## API endpoints

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/students` | Create a student. Returns `201 Created`. |
| `GET` | `/students` | List all students. |
| `GET` | `/students/{student_id}` | Get one student. |
| `PUT` | `/students/{student_id}` | Replace all student fields. |
| `PATCH` | `/students/{student_id}` | Update one or more student fields. |
| `DELETE` | `/students/{student_id}` | Delete a student. |

Requests for an absent student return `404` with:

```json
{"detail": "Student not found"}
```

## Example requests and responses

Create a student:

```http
POST /students
Content-Type: application/json

{
  "name": "Aisha Khan",
  "age": 20,
  "course": "Computer Science"
}
```

Response (`201 Created`):

```json
{
  "id": 1,
  "name": "Aisha Khan",
  "age": 20,
  "course": "Computer Science"
}
```

Partially update a student:

```http
PATCH /students/1
Content-Type: application/json

{
  "course": "Data Science"
}
```

Response (`200 OK`):

```json
{
  "id": 1,
  "name": "Aisha Khan",
  "age": 20,
  "course": "Data Science"
}
```

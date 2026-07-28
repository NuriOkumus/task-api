# Task API

A CRUD API for managing a to-do list, built with **Python**, **FastAPI**, and **SQLite**.

## How to Run

```bash
# 1. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install fastapi uvicorn

# 3. Start the server
uvicorn main:app --reload
```

The database (`tasks.db`) is created automatically on first run. Three example tasks are inserted only once.

Server runs at `http://localhost:8000`

## Database

- **Engine:** SQLite (built into Python, no installation required)
- **File location:** `tasks.db` in the project root
- **Auto-created:** Table is created automatically on startup
- **Seed data:** 3 example tasks are inserted only on the very first run

### Example SQL query

```sql
-- List all completed tasks
SELECT * FROM tasks WHERE done = 1;
```

![SQLite Database](image.png)

## Endpoints

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| GET | `/` | API info | 200 |
| GET | `/health` | Health check | 200 |
| GET | `/tasks` | List all tasks | 200 |
| GET | `/tasks/{id}` | Get single task | 200, 404 |
| POST | `/tasks` | Create a task | 201, 422 |
| PUT | `/tasks/{id}` | Update a task | 200, 404 |
| DELETE | `/tasks/{id}` | Delete a task | 204, 404 |

## Example `curl` Output

```
$ curl -i http://localhost:8000/tasks/1

HTTP/1.1 200 OK
date: Mon, 20 Jul 2026 11:22:45 GMT
server: uvicorn
content-length: 40
content-type: application/json

{"id":1,"title":"Buy milk","done":false}
```

## Swagger UI

Interactive API documentation is available at `http://localhost:8000/docs`

![Swagger UI](brave_screenshot_localhost.png)

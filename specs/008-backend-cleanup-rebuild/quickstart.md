# Quickstart Guide: Backend Cleanup and Rebuild (Phase 2a)

## Prerequisites
- Python 3.13+
- UV package manager
- Access to Neon PostgreSQL database

## Setup Instructions

### 1. Clone and Navigate
```bash
cd /path/to/project
cd backend
```

### 2. Set Up Virtual Environment
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
uv add fastapi sqlmodel uvicorn psycopg2-binary python-jose[cryptography]
```

### 4. Configure Environment Variables
Copy the `.env.example` file and configure your database connection:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

### 5. Initialize the Database
```bash
# Run database initialization
python -c "from database.session import engine; from models.todo import create_db_and_tables; create_db_and_tables()"
```

### 6. Run the Application
```bash
uvicorn main:app --reload
```

## API Endpoints
Once running, the API will be available at `http://localhost:8000` with the following endpoints:
- `GET /api/tasks` - List all tasks
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{id}` - Get a specific task
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion

## Testing the API
You can test the API using curl or any HTTP client:

```bash
# Create a task
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test task", "description": "A sample task"}'

# List all tasks
curl http://localhost:8000/api/tasks
```
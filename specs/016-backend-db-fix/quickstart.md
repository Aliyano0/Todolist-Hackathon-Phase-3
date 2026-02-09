# Quickstart Guide: Backend Database Schema Fix

## Prerequisites
- Python 3.13+
- Node.js 18+ and npm/yarn/pnpm
- Git
- Access to Neon Serverless PostgreSQL database
- UV package manager

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd todolist-hackathon
git checkout 016-backend-db-fix
```

### 2. Install Backend Dependencies
```bash
cd backend
uv venv  # Create virtual environment using UV
source .venv/bin/activate  # Activate virtual environment
uv pip install -r requirements.txt
```

### 3. Install Frontend Dependencies
```bash
cd frontend
npm install
# or yarn install
# or pnpm install
```

### 4. Environment Configuration
Create `.env` file in the backend directory:
```env
NEON_DATABASE_URL=your_neon_database_url
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Run Database Migration
Before starting the application, ensure the database schema is updated:

```bash
cd backend
python -c "from database.migrations import add_priority_category_columns; add_priority_category_columns()"
```

### 6. Start Development Servers

#### Backend (FastAPI)
```bash
cd backend
uv run uvicorn main:app --reload --port 8000
```

The backend will automatically run the migration on startup if needed.

#### Frontend (Next.js)
```bash
cd frontend
npm run dev
# or yarn dev
# or pnpm dev
```

The application will be available at `http://localhost:3000`

## Key Files to Review

### Database Migration Implementation
- `backend/database/migrations.py` - Contains the migration function to add priority and category columns
- `backend/main.py` - Includes the migration call in the lifespan event handler

### Updated Models and Schemas
- `backend/models/todo.py` - Updated TodoTask model with priority and category fields
- `backend/schemas/todo.py` - Updated schemas to include new fields
- `backend/core/services/todo_service.py` - Updated service functions to handle new fields

### API Endpoints
- `backend/api/tasks.py` - Updated API endpoints to handle priority and category fields

## Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
# or yarn test
# or pnpm test
```

## Troubleshooting

### Common Issues

1. **Database Migration Errors**: If you encounter errors during migration, ensure your database connection is working and the Neon Serverless PostgreSQL is accessible.

2. **Missing Columns Error**: If the application still reports missing columns, run the migration script manually:
   ```bash
   python -c "from database.migrations import add_priority_category_columns; add_priority_category_columns()"
   ```

3. **API Endpoint Errors**: Check that all API endpoints properly handle the new priority and category fields.

### Verification Steps
1. Verify the migration ran successfully by checking that the `priority` and `category` columns exist in the `todotask` table
2. Test creating a new todo item with priority and category fields
3. Verify existing todo items have been updated with default priority and category values
4. Test all API endpoints to ensure they return the new fields properly

## Development Workflow
1. Make sure the database migration has been run before starting development
2. Update the models, schemas, and services to properly handle the new fields
3. Test all endpoints to ensure they work with the updated schema
4. Run the full test suite to verify no regressions were introduced
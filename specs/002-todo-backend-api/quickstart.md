# Quickstart Guide: Todo Backend API

## Prerequisites
- Python 3.13+
- UV package manager
- PostgreSQL database (Neon Serverless recommended)
- Better Auth configured on the frontend to generate JWT tokens

## Setup Instructions

1. **Clone the repository and navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Install dependencies using UV**
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install fastapi sqlmodel python-jose[cryptography] uvicorn psycopg2-binary
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file with the following variables:
   DATABASE_URL=postgresql://username:password@host:port/database_name
   JWT_SECRET_KEY=your-super-secret-jwt-key-here
   ```

4. **Initialize the database**
   ```bash
   # Run the database initialization script
   python -c "
   from database.session import engine
   from models.todo import SQLModel
   SQLModel.metadata.create_all(engine)
   "
   ```

## Running the Application

1. **Start the development server**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Access the API**
   - API documentation: `http://localhost:8000/docs`
   - API endpoints: `http://localhost:8000/api/`

## Testing the API

1. **Get a JWT token from Better Auth frontend**

2. **Test creating a task**
   ```bash
   curl -X POST http://localhost:8000/api/user123/tasks \
     -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
     -H "Content-Type: application/json" \
     -d '{"title": "Sample task", "description": "This is a sample task"}'
   ```

3. **Test retrieving tasks**
   ```bash
   curl -X GET http://localhost:8000/api/user123/tasks \
     -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
   ```

## Key Features

- **JWT Authentication**: All endpoints require a valid JWT token from Better Auth
- **User Isolation**: Users can only access their own tasks
- **RESTful API**: Follows standard REST conventions
- **Automatic Documentation**: Swagger UI available at `/docs`
- **Validation**: Input validation using Pydantic models

## Troubleshooting

- **Database Connection Issues**: Ensure PostgreSQL is running and DATABASE_URL is correctly configured
- **JWT Validation Errors**: Verify that the JWT_SECRET_KEY matches the one used by Better Auth
- **User Access Issues**: Confirm that the user_id in the JWT matches the one in the URL path
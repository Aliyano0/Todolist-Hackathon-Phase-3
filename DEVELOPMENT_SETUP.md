# Local Development Setup Guide

This guide explains how to set up and run both the backend and frontend servers locally for the multi-user Todo web application.

## Prerequisites

- **Node.js** (v18 or higher)
- **Python** (v3.13 or higher)
- **npm** or **yarn**
- **PostgreSQL** (or use a local instance)

## Backend Setup

### 1. Navigate to Backend Directory
```bash
cd ../backend  # From the frontend directory
```

### 2. Set up Python Environment
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
# Or if there's no requirements.txt, install from pyproject.toml:
pip install -e .
```

### 3. Database Setup
```bash
# Make sure PostgreSQL is running on your system
# Create a database for the application

# Run database migrations (if any)
python -m alembic upgrade head
# Or initialize the database tables directly through the app
```

### 4. Environment Variables
Create a `.env` file in the backend directory:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todolist_db
SECRET_KEY=your-secret-key-here
JWT_SECRET=your-jwt-secret-here
```

### 5. Start Backend Server
```bash
# Activate your virtual environment first
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run the backend server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend server will be available at `http://localhost:8000`

## Frontend Setup

### 1. Navigate to Frontend Directory
```bash
cd ./frontend  # From the root directory where package.json is located
```

### 2. Install Dependencies
```bash
npm install
# or
yarn install
```

### 3. Environment Variables
Create a `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
```

### 4. Start Frontend Server
```bash
npm run dev
# or
yarn dev
```

The frontend server will be available at `http://localhost:3000`

## Complete Development Setup

### Option 1: Separate Terminals (Recommended)

1. **Terminal 1 - Backend:**
   ```bash
   cd ../backend
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Terminal 2 - Frontend:**
   ```bash
   cd .
   npm run dev
   ```

### Option 2: Using Concurrently (if available)

Create a root `package.json` with concurrent startup:
```json
{
  "name": "todolist-monorepo",
  "scripts": {
    "dev": "concurrently \"npm run dev:backend\" \"npm run dev:frontend\"",
    "dev:backend": "cd ../backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000",
    "dev:frontend": "cd . && npm run dev"
  },
  "devDependencies": {
    "concurrently": "^8.2.0"
  }
}
```

Then run:
```bash
npm install concurrently
npm run dev
```

## API Endpoints

### Backend API
- Base URL: `http://localhost:8000`
- Authentication: `http://localhost:8000/auth/*`
- Todos: `http://localhost:8000/api/todos/*`
- Users: `http://localhost:8000/api/users/*`

### Frontend Routes
- Home: `http://localhost:3000`
- Login: `http://localhost:3000/login`
- Register: `http://localhost:3000/register`
- Dashboard: `http://localhost:3000/dashboard`
- Profile: `http://localhost:3000/profile`

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   - Change ports in the startup commands:
   ```bash
   # For backend
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001

   # For frontend (if 3000 is taken)
   npm run dev -- -p 3001
   ```

2. **Database Connection Issues**
   - Ensure PostgreSQL is running
   - Verify database credentials in `.env`
   - Check that the database exists

3. **Environment Variables Missing**
   - Make sure `.env.local` has the correct API URLs
   - Ensure backend server is accessible from frontend

4. **Dependency Installation Issues**
   - Clear node_modules and reinstall:
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```
   - For Python, recreate the virtual environment:
   ```bash
   rm -rf venv
   python -m venv venv
   source venv/bin/activate
   pip install -e .
   ```

### CORS Configuration
If you encounter CORS issues, make sure the backend allows requests from `http://localhost:3000`:

In your backend's `main.py` or middleware configuration:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Development Tips

1. **Hot Reload**: Both servers support hot reloading during development
2. **API Testing**: You can test backend API endpoints directly at `http://localhost:8000/docs`
3. **Frontend Development**: The Next.js development server provides fast refresh
4. **Environment Sync**: Keep backend and frontend `.env` files synchronized

Once both servers are running, you can access the application at `http://localhost:3000` and begin using the multi-user Todo web application.
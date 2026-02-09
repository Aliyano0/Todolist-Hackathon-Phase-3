#!/bin/bash

# Script to verify backend-frontend integration

echo "Starting backend-frontend integration verification..."

# Test backend server connectivity
echo "Checking backend server..."
BACKEND_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health 2>/dev/null)
if [ "$BACKEND_RESPONSE" = "200" ]; then
    echo "✓ Backend server is reachable"
else
    echo "✗ Backend server is not reachable (HTTP $BACKEND_RESPONSE)"
fi

# Test API endpoint connectivity
echo "Checking API endpoints..."
API_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/todos 2>/dev/null)
if [ "$API_RESPONSE" = "200" ] || [ "$API_RESPONSE" = "401" ] || [ "$API_RESPONSE" = "403" ]; then
    echo "✓ API endpoints are accessible"
else
    echo "✗ API endpoints are not accessible (HTTP $API_RESPONSE)"
fi

# Verify environment configuration
echo "Checking environment configuration..."
if [ -f "./backend/.env" ]; then
    echo "✓ Backend .env file exists"
else
    echo "! Backend .env file not found"
fi

if [ -f "./frontend/.env.local" ]; then
    echo "✓ Frontend .env.local file exists"
else
    echo "! Frontend .env.local file not found"
fi

# Check if required dependencies are installed
echo "Checking dependencies..."
cd ./backend && source .venv/bin/activate 2>/dev/null && python -c "import fastapi, sqlmodel" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ Backend dependencies are installed"
else
    echo "✗ Backend dependencies missing"
fi

cd ../frontend && npm list > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ Frontend dependencies are installed"
else
    echo "✗ Frontend dependencies missing"
fi

cd ..

echo "Integration verification complete!"
echo ""
echo "To run the integrated application:"
echo "1. Terminal 1: cd backend && source .venv/bin/activate && uv run -m uvicorn main:app --reload"
echo "2. Terminal 2: cd frontend && npm run dev"
echo "3. Visit http://localhost:3000 to access the application"
# Quickstart Guide: Todo App Enhancement Development

## Prerequisites
- Node.js 18+ and npm/yarn/pnpm
- Python 3.13+
- Git
- Text editor or IDE

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd todolist-hackathon
git checkout 015-todo-enhancement
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
Create `.env.local` in the frontend directory:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_JWT_SECRET=your-secret-key
```

### 5. Start Development Servers

#### Backend (FastAPI)
```bash
cd backend
uv run uvicorn main:app --reload --port 8000
```

#### Frontend (Next.js)
```bash
cd frontend
npm run dev
# or yarn dev
# or pnpm dev
```

The application will be available at `http://localhost:3000`

## Key Files to Modify

### Fix toggleComplete Error
- `frontend/app/page.tsx` - Main page component where toggleComplete should be defined
- `frontend/components/todo/TodoItem.tsx` - Component where toggleComplete is called

### UI Enhancement Files
- `frontend/components/ui/Button.tsx` - Update button components with animations
- `frontend/styles/globals.css` - Add modern color theme
- `frontend/components/todo/TodoItem.tsx` - Add animations and visual enhancements

### Priority and Category Implementation
- `frontend/lib/api.ts` - Update API functions to handle priority and category
- `frontend/components/todo/TodoForm.tsx` - Add priority and category selection
- `frontend/types/index.ts` - Update TypeScript types for priority and category

## Running Tests
```bash
# Frontend tests
cd frontend
npm test

# Backend tests
cd backend
pytest
```

## Technology Stack
- **Frontend**: Next.js 16.1+, TypeScript, Tailwind CSS, Shadcn UI, Framer Motion
- **Backend**: FastAPI, Python 3.13+, SQLModel, Neon Serverless PostgreSQL
- **Authentication**: Better Auth with JWT tokens
- **State Management**: React hooks and local storage

## Development Workflow
1. Start by fixing the toggleComplete function error in `app/page.tsx`
2. Test that task completion works properly
3. Implement UI enhancements with shadcn UI and Motion animations
4. Add priority and category features
5. Ensure all existing functionality remains intact
6. Run tests to verify all features work correctly

## Troubleshooting
- If toggleComplete error persists: Check function definition and export in the correct module
- If animations are janky: Optimize components and ensure Motion is properly configured
- If data persistence fails: Verify JWT token handling and local storage operations
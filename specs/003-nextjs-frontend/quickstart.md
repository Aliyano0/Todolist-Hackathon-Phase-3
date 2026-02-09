# Quickstart Guide: Next.js Frontend for Multi-User Todo Web App

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Access to the backend API (running FastAPI server)

## Setup Instructions

### 1. Clone and Navigate
```bash
# If not already done, create the frontend directory
mkdir frontend
cd frontend
```

### 2. Initialize Next.js Project
```bash
npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
```

### 3. Install Dependencies
```bash
npm install @radix-ui/react-slot lucide-react
npm install -D tailwindcss-animate
npm install better-auth
```

### 4. Configure Tailwind CSS
The configuration should already be set up by the create-next-app command.

### 5. Environment Variables
Create a `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_JWT_SECRET=your_jwt_secret_here
```

## Development Workflow

### 1. Run the Development Server
```bash
npm run dev
```

### 2. Key File Locations
- **Pages**: `src/app/` - Contains all route pages
- **Components**: `src/components/` - Reusable UI components
- **API Client**: `src/lib/api.ts` - API communication logic
- **Auth Provider**: `src/providers/AuthProvider.tsx` - Authentication context
- **Styles**: `src/app/globals.css` - Global styles and Tailwind directives

## Authentication Flow

1. **Registration**: Users register via `/register` page
2. **Login**: Users authenticate via `/login` page
3. **Protected Routes**: Dashboard and other user-specific pages require authentication
4. **Token Management**: JWT tokens are stored in memory/context and attached to API requests
5. **Auto-refresh**: Tokens are silently refreshed before expiration
6. **Session Timeout**: Users are logged out after 30 minutes of inactivity

## Todo Operations

### Creating Todos
- Use the TodoForm component to create new todos
- Title is required, description is optional (max 500 characters)
- Created todos are automatically associated with the authenticated user

### Viewing Todos
- Todos are filtered by the authenticated user's ID
- The TodoList component displays all user's todos

### Updating Todos
- Use the TodoItem component to update todo properties
- Changes are synced with the backend via API calls

### Deleting Todos
- Each TodoItem has a delete button
- Deletion is confirmed before executing the API call

## Theming

The application supports light and dark themes:
- Theme preference is stored in localStorage
- Theme is applied globally via CSS variables
- Users can toggle between themes using the theme switcher component

## API Integration

All API calls follow this pattern:
1. Check authentication status
2. Attach JWT token to request headers
3. Handle response/error cases
4. Update local state accordingly

Example API call:
```typescript
const response = await fetch('/api/todos', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${authToken}`,
    'Content-Type': 'application/json'
  }
});
```

## Testing

Run the test suite with:
```bash
npm run test
```

Tests should cover:
- Component rendering
- User interactions
- API integration
- Authentication flows
- Error handling
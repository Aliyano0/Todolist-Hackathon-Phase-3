# Quickstart Guide: Frontend Rebuild

## Overview
This guide provides instructions for setting up and running the rebuilt frontend application from scratch.

## Prerequisites
- Node.js 18+ installed
- npm or yarn package manager
- Access to the backend API (Phase 2a) running on localhost:8000

## Setup Instructions

### 1. Clean Frontend Directory Creation
First, ensure the old frontend directory is completely removed and create a new one:
```bash
rm -rf frontend
mkdir frontend
cd frontend
```

### 2. Initialize Next.js Project
```bash
npx create-next-app@latest .
# Select options:
# - Yes for TypeScript
# - Yes for Tailwind CSS
# - No for src directory
# - Yes for App Router
# - No for linting
# - No for tests
# - No for app directory (we'll use the new App Router)
```

### 3. Install Dependencies
```bash
npm install -D tailwindcss postcss autoprefixer
npm install next react react-dom
npm install @radix-ui/react-slot lucide-react
npm install clsx tailwind-merge
```

### 4. Install Shadcn UI
```bash
npx shadcn-ui@latest init
npx shadcn-ui@latest add button card input label
```

### 5. Environment Configuration
Create a `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME="Todo Application"
```

### 6. Run Development Server
```bash
npm run dev
```

The application will be available at http://localhost:3000

## Project Structure
```
frontend/
├── app/                 # Next.js 16.1 App Router pages
│   ├── layout.tsx       # Root layout with theme provider
│   ├── page.tsx         # Main Todo dashboard page
│   ├── profile/         # Profile page with theme settings
│   │   └── page.tsx
│   ├── globals.css      # Global styles and Tailwind imports
│   └── providers/       # React context providers
│       └── theme-provider.tsx
├── components/          # Reusable UI components
│   ├── todo/            # Todo-specific components
│   │   ├── TodoForm.tsx
│   │   ├── TodoItem.tsx
│   │   ├── TodoList.tsx
│   │   └── TodoActions.tsx
│   ├── ui/              # Shadcn UI components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   └── ...
│   ├── theme/           # Theme toggle components
│   │   └── ThemeToggle.tsx
│   └── navigation/      # Navigation components
│       └── Navbar.tsx
├── lib/                 # Utility functions
│   ├── api.ts           # API client for backend integration
│   ├── utils.ts         # General utility functions
│   └── theme.ts         # Theme-related utilities
├── hooks/               # Custom React hooks
│   └── useTodos.ts      # Todo management hooks
├── public/              # Static assets
│   └── favicon.ico
├── package.json
├── next.config.ts
├── tailwind.config.ts
└── tsconfig.json
```

## Key Features Setup

### 1. Theme Management
The application supports light/dark mode with the following implementation:
- Theme state is managed using React Context
- Preference is stored in localStorage
- Theme persists across sessions
- Automatic system preference detection

### 2. Todo Operations
The application supports 5 basic Todo operations:
- **Add**: Create new todo items via form
- **View**: Display all todos with filtering options
- **Update**: Modify todo title or description
- **Delete**: Remove todo items permanently
- **Mark Complete**: Toggle completion status

### 3. Responsive Design
The UI is responsive across different screen sizes:
- Mobile: 320px-768px
- Tablet: 768px-1024px
- Desktop: 1024px+

### 4. API Integration
The frontend integrates with the backend API using standard endpoints:
- GET `/todos` - Retrieve all todos
- POST `/todos` - Create new todo
- PUT `/todos/{id}` - Update todo
- DELETE `/todos/{id}` - Delete todo
- PATCH `/todos/{id}/toggle` - Mark complete/incomplete

## Running Tests
```bash
npm run test
# or for watch mode
npm run test:watch
```

## Building for Production
```bash
npm run build
```

## Deployment
The application can be deployed to any platform that supports Next.js applications (Vercel, Netlify, etc.).

## Troubleshooting

### Common Issues
1. **API Connection Errors**: Ensure the backend API is running on the configured URL
2. **Theme Not Persisting**: Check that localStorage is enabled in the browser
3. **Styles Not Loading**: Verify Tailwind CSS is properly configured

### Development Tips
- Use the Next.js development server for hot reloading
- Check browser console for any runtime errors
- Use React Developer Tools for debugging component state
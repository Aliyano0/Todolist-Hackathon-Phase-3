# Quickstart Guide: Next.js Frontend for Todo Application

## Prerequisites
- Node.js 18+ installed
- Access to backend API running at http://localhost:8000

## Setup Instructions

### 1. Clone and Navigate
```bash
cd frontend
```

### 2. Install Dependencies
```bash
npm install
# or
yarn install
# or
pnpm install
```

### 3. Environment Configuration
Create a `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
```

### 4. Run Development Server
```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

Visit `http://localhost:3000` to see the application.

## Key Commands

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run linter
- `npm run test` - Run tests

## Project Structure Overview

```
frontend/
├── app/                 # Next.js App Router pages
├── components/         # Reusable React components
├── lib/               # Utilities and API clients
├── hooks/             # Custom React hooks
├── providers/         # Context providers
└── tests/             # Test files
```

## Running Tests

Unit and integration tests:
```bash
npm run test
```

End-to-end tests:
```bash
npm run test:e2e
```

## Key Features

1. **Todo Operations**: Add, view, update, delete, and mark complete/incomplete
2. **Theme Switching**: Light/dark mode toggle with system preference detection
3. **Responsive Design**: Works on mobile, tablet, and desktop
4. **Optimistic Updates**: Instant UI feedback with backend synchronization
5. **Error Handling**: Graceful degradation with user feedback

## API Integration

The frontend communicates with the backend via REST API endpoints as defined in the contracts. The API client is located in `lib/api.ts` and handles:
- Request/response handling
- Error management
- Loading states
- Optimistic updates
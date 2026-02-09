# Quickstart Guide: Frontend Fixes and Improvements

## Prerequisites
- Node.js 18+ and npm
- Access to backend API running on http://localhost:8000

## Setup
1. Install dependencies: `npm install`
2. Set environment variables in `.env.local`:
   ```
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   NEXT_PUBLIC_APP_NAME="Todo Application"
   ```
3. Start the development server: `npm run dev`

## Running Tests
- Unit tests: `npm run test`
- Integration tests: `npm run test:integration`
- End-to-end tests: `npm run test:e2e`

## Key Commands
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run linter
- `npm run type-check` - Run type checker

## Environment Variables
- `NEXT_PUBLIC_API_BASE_URL` - Backend API URL (default: http://localhost:8000)
- `NEXT_PUBLIC_APP_NAME` - Application name (default: "Todo Application")

## Troubleshooting
- If tasks don't appear, ensure backend API is running
- For styling issues, check Tailwind CSS configuration
- For 404 errors on /todos route, verify route exists in app directory
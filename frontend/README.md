# Todo Frontend Application

This is the frontend for the Todo application built with Next.js 16.1 and App Router.

## Features

- Next.js 16.1 with App Router
- Responsive design with Tailwind CSS
- Light and dark theme support
- Todo management (Create, Read, Update, Delete, Toggle completion)
- Clean architecture with proper separation of concerns

## Getting Started

First, install the dependencies:

```bash
npm install
```

Then, run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the application.

## Environment Variables

Create a `.env.local` file in the root of the project and add the following:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME="Todo Application"
```

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
├── tsconfig.json
└── CLAUDE.md            # Frontend-specific Claude instructions
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
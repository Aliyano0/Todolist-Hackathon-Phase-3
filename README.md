# The Evolution of Todo - Phase 1

A simple in-memory todo console application built with clean architecture principles.

## Features

- Add tasks with title and optional description
- List all tasks with completion status indicators
- View individual task details
- Mark tasks as complete/incomplete (bug fixed)
- Update task title and/or description
- Delete tasks
- **Interactive Mode** - Menu-driven session for easy task management
- **Modern UI Design** - Updated with modern color theme and smooth animations
- **Priority Management** - Tasks can have priority levels (high, medium, low)
- **Category Management** - Tasks can be categorized (work, personal, shopping, or custom)
- **Advanced Filtering** - Sort and filter tasks by priority, category, and completion status
- **Glowing Effects** - Animated buttons with glowing effects for better UX

## Requirements

- Python 3.13+ (backend)
- Node.js 18+ and npm/yarn/pnpm (frontend)
- UV package manager

## Backend Installation

```bash
# Install the package in development mode
uv pip install -e .
```

## Frontend Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   # or
   pnpm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   # or
   pnpm dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser to see the result.

## Usage

### Quick Start (Single Command)

```bash
# Add a new task
todolist add "Buy groceries" -d "Milk, eggs, bread"

# List all tasks
todolist list
```


### Interactive Mode

Enter an interactive menu-driven session to manage tasks without typing full commands:

```bash
# Enter interactive mode
todolist interactive
```

**Menu Options:**
```
Menu:
  1. Add Task
  2. List Tasks
  3. Get Task Details
  4. Update Task
  5. Mark Complete/Incomplete
  6. Delete Task
  7. Exit
```

**Example Session:**
```
$ todolist interactive
==================================================
         Todo List - Interactive Mode
==================================================

Menu:
  1. Add Task
  2. List Tasks
  3. Get Task Details
  4. Update Task
  5. Mark Complete/Incomplete
  6. Delete Task
  7. Exit

Enter your choice (1-7): 1
Enter task title: Buy groceries
Enter task description (optional): Milk, eggs, bread
Added task 1: "Buy groceries"

Menu:
  1. Add Task
  ...
```

### All Commands

```bash
# Show compact output
todolist list --simple

# View task details
todolist get 1

# Mark task as complete
todolist mark 1 --complete

# Mark task as incomplete
todolist mark 1 --incomplete

# Update task title
todolist update 1 --title "New title"

# Update task description
todolist update 1 -d "New description"

# Delete a task
todolist delete 1

# Enter interactive mode
todolist interactive

# Show help
todolist --help

# Show version
todolist --version
```

## Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=term-missing

# Run specific test file
uv run pytest tests/unit/use_cases/test_add_todo.py -v
```

## Project Structure

```
todolist-phase-1/
├── src/
│   └── core/
│       ├── entities/
│       │   └── todo.py           # Todo domain entity
│       ├── exceptions/
│       │   └── todo_errors.py    # Domain exceptions
│       ├── ports/
│       │   └── repository.py     # Repository port (interface)
│       └── use_cases/
│           ├── add_todo.py       # Add todo use case
│           ├── list_todos.py     # List todos use case
│           ├── get_todo.py       # Get todo use case
│           ├── update_todo.py    # Update todo use case
│           ├── delete_todo.py    # Delete todo use case
│           └── mark_complete.py  # Mark complete use case
├── adapters/
│   ├── cli/
│   │   └── __main__.py           # CLI entry point
│   └── repository/
│       └── memory_repository.py  # In-memory repository implementation
├── tests/
│   ├── unit/
│   │   ├── entities/
│   │   ├── ports/
│   │   └── use_cases/
│   └── integration/
│       └── test_cli_flow.py      # Full workflow integration tests
├── specs/
│   └── 001-todo-console-app/
│       ├── spec.md               # Feature specification
│       ├── plan.md               # Architecture plan
│       └── tasks.md              # Task breakdown
├── pyproject.toml
└── README.md
```

## Architecture

This project follows Clean Architecture with:

- **Entities**: Domain objects with validation logic
- **Use Cases**: Business logic encapsulated in single-responsibility classes
- **Ports**: Abstract interfaces for external dependencies
- **Adapters**: Concrete implementations (CLI, repository)

This separation enables easy testing and future evolution (e.g., adding persistence).

## Phase Roadmap

- **Phase 1**: In-memory console app (current)
- **Phase 2**: Multi-user web application with persistent storage (ongoing)
  - Backend: FastAPI with Python 3.13+
  - Frontend: Next.js 16.1 with App Router
  - Database: Neon Serverless PostgreSQL with SQLModel ORM
  - Authentication: Better Auth with JWT integration
- **Phase 3**: Enhanced features and scalability
- **Phase 4**: Mobile application
- **Phase 5**: Advanced analytics and insights

## Documentation Structure

- **Root CLAUDE.md**: Global instructions applicable to the entire project
- **Backend CLAUDE.md**: Context-specific instructions for backend development
- **Frontend CLAUDE.md**: Context-specific instructions for frontend development

## Production Deployment

Ready to deploy your Todo application to production? We've created comprehensive guides for deploying both frontend and backend:

### Deployment Guides

- **[Hugging Face Spaces Deployment](docs/deployment/huggingface.md)** - Deploy backend API with Docker
- **[Vercel Deployment](docs/deployment/vercel.md)** - Deploy Next.js frontend
- **[Environment Variables Reference](docs/deployment/environment.md)** - Complete configuration guide

### Production Guides

- **[Security Checklist](docs/production/security.md)** - Pre-deployment security review
- **[Monitoring Guide](docs/production/monitoring.md)** - Set up monitoring and alerts

### Quick Deployment Steps

1. **Set up Database**: Create Neon PostgreSQL database
2. **Configure SMTP**: Set up email service (Gmail, SendGrid, etc.)
3. **Deploy Backend**: Push to Hugging Face Spaces with environment variables
4. **Deploy Frontend**: Deploy to Vercel with API URL
5. **Test End-to-End**: Verify authentication and password reset flow

See the deployment guides for detailed step-by-step instructions.

---

**Built with ❤️ using Python, FastAPI, Next.js, and deployed on Hugging Face Spaces + Vercel**

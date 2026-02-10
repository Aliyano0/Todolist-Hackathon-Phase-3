---
name: fastapi-basics
description: Guide for setting up and running a basic FastAPI application, including installation, main app creation, and running the server. Use this when the user asks about starting with FastAPI or basic setup.
---

## Instructions for FastAPI Basics

When assisting with FastAPI basic setup:

1. **Installation**:
   - Install with Uv add: `uv add fastapi uvicorn`.
   - For full features: `uv add "fastapi[all]"`.

2. **Creating the App**:
   - Import FastAPI: `from fastapi import FastAPI`.
   - Instantiate: `app = FastAPI()`.

3. **Basic Endpoint**:
   - Define a GET route: `@app.get("/") def root(): return {"message": "Hello World"}`.

4. **Running the Server**:
   - Use Uvicorn: `uvicorn main:app --reload` (assuming file is main.py).
   - Access at http://127.0.0.1:8000.

5. **Interactive Docs**:
   - Swagger UI at /docs.
   - ReDoc at /redoc.

6. **Best Practices**:
   - Use virtual environments (venv or poetry).
   - Structure project with main.py and separate modules.
   - Enable debug mode for development: `app = FastAPI(debug=True)`.

## References

Use the shared references located at:
../_shared/reference.md

---
name: fastapi-routing
description: Guidance on defining routes, path parameters, query parameters, and HTTP methods in FastAPI. Activate for questions about endpoints, URLs, or handling requests.
---

## Instructions for FastAPI Routing

Handle FastAPI routing as follows:

1. **Path Operations**:
   - Use decorators: `@app.get("/items/{item_id}")`, `@app.post("/items/")`, etc.
   - Support GET, POST, PUT, DELETE, PATCH, OPTIONS, HEAD, TRACE.

2. **Path Parameters**:
   - Define in path: `{item_id}`.
   - Type hint: `def get_item(item_id: int): ...`.
   - Validation: Automatic type conversion and error handling.

3. **Query Parameters**:
   - Not in path: `def list_items(skip: int = 0, limit: int = 10): ...`.
   - Optional: Use `= None` or `Query(None)` for advanced.

4. **Request Body**:
   - Use Pydantic models: `from pydantic import BaseModel`.
   - `def create_item(item: Item): ...` where Item is a BaseModel.

5. **Advanced Routing**:
   - Path converters: `{item_id:uuid}`.
   - Sub-applications: `app.include_router(router, prefix="/api/v1")`.

6. **Best Practices**:
   - Keep routes organized in routers.
   - Handle status codes: `return {"item": item}, status_code=201`.
   - Use enums for fixed values.

## References

Use the shared references located at:
../_shared/reference.md

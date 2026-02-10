---
name: fastapi-dependencies
description: Step-by-step guide for using dependencies, dependency injection, and caching in FastAPI. Trigger for queries about reusable logic, auth checks, or database sessions.
---

## Instructions for FastAPI Dependencies

Manage dependencies in FastAPI:

1. **Defining Dependencies**:
   - Functions: `def common_parameters(q: str = None): return {"q": q}`.
   - Classes: With `__call__` method.

2. **Injection**:
   - In paths: `@app.get("/items/", dependencies=[Depends(common_parameters)])`.
   - In params: `def get_items(commons: dict = Depends(common_parameters)): ...`.

3. **Sub-Dependencies**:
   - Nest: `def sub_dep(): ...` then `def main_dep(sub=Depends(sub_dep)): ...`.

4. **Caching**:
   - Automatic per request.
   - Override with `cached=False` in Depends.

5. **Scopes**:
   - Application, router, or path level.
   - Use for DB sessions: Yield for cleanup.

6. **Best Practices**:
   - Use for authentication, logging, rate limiting.
   - Async dependencies for async code.
   - Test dependencies separately.

## References

Use the shared references located at:
../_shared/reference.md

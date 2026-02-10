---
name: fastapi-request-response
description: Instructions for handling requests, responses, headers, cookies, and file uploads in FastAPI. Use when the query involves data validation, responses, or request components.
---

## Instructions for FastAPI Request and Response

For request and response handling in FastAPI:

1. **Request Object**:
   - Inject: `from fastapi import Request`.
   - `@app.get("/") async def root(request: Request): ...`.

2. **Response Models**:
   - Declare: `@app.get("/items/{item_id}", response_model=Item)`.
   - Use Pydantic for validation and serialization.

3. **Headers and Cookies**:
   - Headers: `from fastapi import Header`.
   - `def get_header(x_token: str = Header(None)): ...`.
   - Cookies: `from fastapi import Cookie`.
   - Set in response: `Response.set_cookie(key="session", value="abc")`.

4. **File Uploads**:
   - `from fastapi import File, UploadFile`.
   - `async def upload(file: UploadFile = File(...)): contents = await file.read()`.

5. **Custom Responses**:
   - Return JSONResponse, HTMLResponse, etc.
   - Streaming: `StreamingResponse(generator())`.

6. **Best Practices**:
   - Validate with Pydantic: Add validators with `@validator`.
   - Handle errors with HTTPException.
   - Use response_model_exclude for sensitive data.

## References

Use the shared references located at:
../_shared/reference.md

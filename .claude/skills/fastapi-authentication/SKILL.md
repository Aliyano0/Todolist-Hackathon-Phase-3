---
name: fastapi-authentication
description: Guidance on implementing authentication and security in FastAPI, including OAuth2, JWT, and API keys. Use for security, users, or access control queries.
---

## Instructions for FastAPI Authentication

Implement authentication in FastAPI:

1. **Security Schemes**:
   - Import: `from fastapi.security import OAuth2PasswordBearer`.
   - Define: `oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")`.

2. **API Keys**:
   - Header: `api_key = APIKeyHeader(name="X-API-KEY")`.
   - Query or Cookie similarly.

3. **JWT**:
   - Use PyJWT: Encode/decode tokens.
   - Dependency: `def get_current_user(token: str = Depends(oauth2_scheme)): ...`.

4. **OAuth2 Flows**:
   - Password flow: `@app.post("/token")` returning access_token.
   - Integrate with databases for users.

5. **Scopes**:
   - `Security(oauth2_scheme, scopes=["read:items"])`.

6. **Best Practices**:
   - Hash passwords with passlib or bcrypt.
   - Use HTTPS in production.
   - Handle token expiration and refresh.


## References

Use the shared references located at:
../_shared/reference.md

# Research: Production Deployment Configuration

**Feature**: 019-production-deployment
**Date**: 2026-02-09
**Status**: Complete

## Overview

This document captures research findings for production deployment of the Todo application, including Docker containerization, SMTP email integration, and platform-specific configurations for Vercel (frontend) and Hugging Face Spaces (backend).

## Research Areas

### 1. Docker Containerization for FastAPI

**Decision**: Use multi-stage Docker build with Python 3.13 slim base image

**Rationale**:
- Multi-stage builds reduce final image size by excluding build dependencies
- Python 3.13 slim provides minimal footprint while maintaining compatibility
- Official Python images are well-maintained and secure
- Separating build and runtime stages improves security (no build tools in production)

**Alternatives Considered**:
- **Alpine Linux base**: Rejected due to musl libc compatibility issues with some Python packages
- **Full Python image**: Rejected due to large size (900MB+ vs 150-200MB for slim)
- **Distroless images**: Rejected due to debugging complexity and limited tooling

**Best Practices**:
- Use `.dockerignore` to exclude unnecessary files (tests, .git, __pycache__)
- Install dependencies in separate layer for better caching
- Run application as non-root user for security
- Use HEALTHCHECK instruction for container monitoring
- Set proper environment variables for production mode
- Use uvicorn with multiple workers for production

**Implementation Notes**:
```dockerfile
# Build stage: Install dependencies
FROM python:3.13-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Runtime stage: Copy only necessary files
FROM python:3.13-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8000
HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

---

### 2. SMTP Email Service Integration

**Decision**: Use `aiosmtplib` for async SMTP email sending

**Rationale**:
- Native async/await support integrates seamlessly with FastAPI
- Non-blocking email sending prevents request timeout issues
- Well-maintained library with good documentation
- Supports TLS/SSL for secure email transmission
- Compatible with all major SMTP providers (Gmail, SendGrid, AWS SES, etc.)

**Alternatives Considered**:
- **smtplib (stdlib)**: Rejected due to blocking I/O (would block FastAPI event loop)
- **python-email**: Rejected as it's just email formatting, not sending
- **sendgrid-python**: Rejected as it locks us into SendGrid (want provider flexibility)
- **boto3 (AWS SES)**: Rejected as it locks us into AWS

**Best Practices**:
- Use connection pooling for multiple emails
- Implement retry logic with exponential backoff
- Log email sending attempts without exposing content
- Use HTML email templates with plain text fallback
- Include unsubscribe links for transactional emails (future)
- Validate email addresses before sending
- Handle SMTP errors gracefully (don't expose to users)

**Configuration Requirements**:
```python
SMTP_HOST: str          # e.g., smtp.gmail.com
SMTP_PORT: int          # e.g., 587 for TLS, 465 for SSL
SMTP_USERNAME: str      # SMTP authentication username
SMTP_PASSWORD: str      # SMTP authentication password
SMTP_FROM_EMAIL: str    # Sender email address
SMTP_FROM_NAME: str     # Sender display name
SMTP_USE_TLS: bool      # Use STARTTLS (recommended)
```

**Email Template Structure**:
- Subject: "Reset Your Password - Todo App"
- HTML body with branded header, reset button, plain link fallback
- Security notice: "If you didn't request this, ignore this email"
- Expiration notice: "This link expires in 1 hour"
- Plain text alternative for email clients without HTML support

---

### 3. Hugging Face Spaces Deployment

**Decision**: Deploy as Docker Space with persistent storage for database connection

**Rationale**:
- Docker Spaces support custom Dockerfile (full control over environment)
- Supports environment variables for secrets management
- Provides persistent storage for logs and temporary files
- Auto-scaling based on usage (within resource limits)
- Built-in HTTPS and domain provisioning
- Free tier available for testing

**Requirements**:
- Dockerfile in repository root or backend/ directory
- README.md with Space configuration in frontmatter
- Environment variables configured in Space settings
- Database connection string accessible from Hugging Face network

**Configuration**:
```yaml
# README.md frontmatter
---
title: Todo Backend API
emoji: ✅
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---
```

**Environment Variables**:
- `DATABASE_URL`: Neon PostgreSQL connection string
- `JWT_SECRET_KEY`: Secret for JWT token signing
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`: Email configuration
- `FRONTEND_URL`: Vercel frontend URL for CORS
- `ENVIRONMENT`: Set to "production"

**Deployment Process**:
1. Push code to GitHub repository
2. Create new Space on Hugging Face
3. Connect GitHub repository to Space
4. Configure environment variables in Space settings
5. Space automatically builds and deploys Docker container
6. Monitor logs for startup issues

**Limitations**:
- CPU: 2 vCPU (free tier)
- Memory: 16GB RAM (free tier)
- Storage: 50GB persistent storage
- No GPU required for this application
- Cold start time: 30-60 seconds if inactive

---

### 4. Vercel Frontend Deployment

**Decision**: Deploy Next.js frontend to Vercel with environment variables for API URL

**Rationale**:
- Vercel is built for Next.js (same company, best integration)
- Automatic HTTPS and CDN distribution
- Zero-config deployment from GitHub
- Environment variable management built-in
- Preview deployments for pull requests
- Edge network for low latency globally

**Configuration**:
```bash
# .env.production (not committed)
NEXT_PUBLIC_API_URL=https://username-todo-backend.hf.space
```

**Build Settings**:
- Framework Preset: Next.js
- Build Command: `npm run build` (default)
- Output Directory: `.next` (default)
- Install Command: `npm install` (default)
- Node Version: 18.x or higher

**Environment Variables** (configured in Vercel dashboard):
- `NEXT_PUBLIC_API_URL`: Backend API URL (Hugging Face Space URL)

**Deployment Process**:
1. Push code to GitHub repository
2. Import project in Vercel dashboard
3. Configure environment variables
4. Deploy (automatic on push to main branch)
5. Verify deployment at provided URL

**Best Practices**:
- Use `NEXT_PUBLIC_` prefix for client-side environment variables
- Configure custom domain if needed
- Enable automatic deployments for main branch
- Use preview deployments for testing branches
- Monitor build logs for errors

---

### 5. Production Security Hardening

**Decision**: Implement comprehensive security headers and configuration

**Security Headers Required**:
```python
# FastAPI middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL")],  # Specific origin only
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Security headers
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response
```

**Configuration Security**:
- All secrets in environment variables (never in code)
- Strong JWT secret (32+ random characters)
- SMTP credentials stored securely
- Database connection string with SSL mode
- Rate limiting on authentication endpoints
- Input validation on all endpoints

**Logging Security**:
- Never log passwords, tokens, or sensitive data
- Sanitize user input in logs
- Use structured logging (JSON format)
- Log levels: INFO for requests, ERROR for failures
- Include request IDs for tracing

---

### 6. Email Template Design

**Decision**: Use HTML email templates with inline CSS and plain text fallback

**Template Structure**:
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #4F46E5;">Reset Your Password</h1>
        <p>You requested to reset your password for your Todo App account.</p>
        <p>Click the button below to reset your password:</p>
        <a href="{reset_url}" style="display: inline-block; padding: 12px 24px; background-color: #4F46E5; color: white; text-decoration: none; border-radius: 4px;">Reset Password</a>
        <p>Or copy and paste this link into your browser:</p>
        <p style="word-break: break-all;">{reset_url}</p>
        <p><strong>This link will expire in 1 hour.</strong></p>
        <p style="color: #666; font-size: 14px;">If you didn't request this password reset, you can safely ignore this email. Your password will not be changed.</p>
    </div>
</body>
</html>
```

**Plain Text Alternative**:
```
Reset Your Password

You requested to reset your password for your Todo App account.

Click the link below to reset your password:
{reset_url}

This link will expire in 1 hour.

If you didn't request this password reset, you can safely ignore this email. Your password will not be changed.
```

**Best Practices**:
- Use inline CSS (many email clients strip `<style>` tags)
- Keep width under 600px for mobile compatibility
- Use web-safe fonts (Arial, Helvetica, sans-serif)
- Test in multiple email clients (Gmail, Outlook, Apple Mail)
- Include both HTML and plain text versions
- Use descriptive link text (not "click here")
- Include security notice about ignoring if not requested

---

## Technology Stack Summary

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Container | Docker | 24.0+ | Backend containerization |
| Base Image | python:3.13-slim | 3.13 | Minimal Python runtime |
| Email Library | aiosmtplib | 3.0+ | Async SMTP email sending |
| Email Formatting | email (stdlib) | - | MIME message construction |
| Backend Platform | Hugging Face Spaces | - | Docker container hosting |
| Frontend Platform | Vercel | - | Next.js serverless hosting |
| Security | FastAPI middleware | - | CORS, security headers |

---

## Risk Analysis

### High Priority Risks

1. **Email Delivery Failures**
   - Risk: SMTP service unavailable or rate limited
   - Mitigation: Implement retry logic, queue failed emails, monitor delivery rates
   - Fallback: Log token to admin console for manual delivery

2. **Database Connection from Hugging Face**
   - Risk: Neon database not accessible from Hugging Face network
   - Mitigation: Test connection during deployment, ensure SSL mode enabled
   - Fallback: Use connection pooling with retry logic

3. **Environment Variable Misconfiguration**
   - Risk: Missing or incorrect environment variables cause startup failure
   - Mitigation: Validate all required variables on startup, fail fast with clear error
   - Fallback: Provide comprehensive error messages and documentation

### Medium Priority Risks

4. **Docker Image Size**
   - Risk: Large image causes slow deployments
   - Mitigation: Use multi-stage builds, minimize dependencies
   - Impact: Deployment time increases but functionality unaffected

5. **CORS Misconfiguration**
   - Risk: Frontend cannot reach backend due to CORS errors
   - Mitigation: Test CORS configuration thoroughly, use specific origins
   - Fallback: Temporarily allow all origins for debugging (not production)

### Low Priority Risks

6. **Cold Start Latency**
   - Risk: First request after inactivity takes 30-60 seconds
   - Mitigation: Implement health check pings, accept as platform limitation
   - Impact: User experience degraded for first user after idle period

---

## Open Questions

None - all technical decisions have been made and documented above.

---

## References

- [FastAPI Docker Documentation](https://fastapi.tiangolo.com/deployment/docker/)
- [aiosmtplib Documentation](https://aiosmtplib.readthedocs.io/)
- [Hugging Face Spaces Docker Guide](https://huggingface.co/docs/hub/spaces-sdks-docker)
- [Vercel Next.js Deployment](https://vercel.com/docs/frameworks/nextjs)
- [OWASP Security Headers](https://owasp.org/www-project-secure-headers/)
- [Email Template Best Practices](https://www.campaignmonitor.com/css/)

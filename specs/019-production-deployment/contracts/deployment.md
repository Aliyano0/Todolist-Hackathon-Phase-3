# Deployment Configuration Contract

**Feature**: 019-production-deployment
**Date**: 2026-02-09
**Version**: 1.0.0

## Overview

This contract defines the deployment configuration requirements for both frontend (Vercel) and backend (Hugging Face Spaces) platforms, including environment variables, build settings, and platform-specific requirements.

---

## Backend Deployment (Hugging Face Spaces)

### Platform Requirements

**Platform**: Hugging Face Spaces with Docker SDK
**Runtime**: Docker container (Linux)
**Base Image**: python:3.13-slim
**Deployment Method**: Git push to connected repository

### Dockerfile Contract

**Location**: `backend/Dockerfile`

**Required Stages**:
1. **Builder Stage**: Install Python dependencies
2. **Runtime Stage**: Copy application code and dependencies

**Required Instructions**:
```dockerfile
# Builder stage
FROM python:3.13-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Runtime stage
FROM python:3.13-slim
WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Set PATH
ENV PATH=/root/.local/bin:$PATH

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

**Optimization Requirements**:
- MUST use multi-stage build to reduce image size
- MUST use `.dockerignore` to exclude unnecessary files
- MUST run as non-root user (future enhancement)
- SHOULD minimize layers for faster builds
- SHOULD use build cache effectively

**Image Size Target**: < 200MB

---

### Environment Variables (Backend)

**Required Variables**:

| Variable | Type | Required | Secret | Description |
|----------|------|----------|--------|-------------|
| `DATABASE_URL` | string | Yes | Yes | PostgreSQL connection string |
| `JWT_SECRET_KEY` | string | Yes | Yes | JWT signing secret (min 32 chars) |
| `SMTP_HOST` | string | Yes | No | SMTP server hostname |
| `SMTP_PORT` | integer | No | No | SMTP server port (default: 587) |
| `SMTP_USERNAME` | string | Yes | No | SMTP authentication username |
| `SMTP_PASSWORD` | string | Yes | Yes | SMTP authentication password |
| `SMTP_FROM_EMAIL` | string | Yes | No | Sender email address |
| `SMTP_FROM_NAME` | string | No | No | Sender display name (default: "Todo App") |
| `FRONTEND_URL` | string | Yes | No | Frontend URL for CORS |
| `ENVIRONMENT` | string | No | No | Environment name (default: "production") |

**Optional Variables**:

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `PORT` | integer | 8000 | Application port |
| `WORKERS` | integer | 4 | Uvicorn worker processes |
| `LOG_LEVEL` | string | INFO | Logging level |
| `LOG_FORMAT` | string | json | Log format (json/text) |
| `RATE_LIMIT_ENABLED` | boolean | true | Enable rate limiting |
| `RATE_LIMIT_PER_MINUTE` | integer | 60 | Rate limit threshold |
| `JWT_ALGORITHM` | string | HS256 | JWT signing algorithm |
| `JWT_EXPIRY_DAYS` | integer | 7 | JWT token expiry |
| `SMTP_USE_TLS` | boolean | true | Use STARTTLS |
| `SMTP_TIMEOUT` | integer | 30 | SMTP timeout in seconds |

**Validation**:
- Application MUST validate all required variables on startup
- Application MUST fail fast with clear error if variables missing
- Application MUST validate variable formats (URLs, emails, integers)
- Application MUST validate secret lengths (JWT secret ≥ 32 chars)

---

### Health Check Endpoint

**Endpoint**: `GET /health`

**Response** (Success):
```json
{
  "status": "healthy",
  "timestamp": "2026-02-09T12:00:00Z",
  "version": "1.0.0",
  "database": "connected",
  "smtp": "configured"
}
```

**Response** (Unhealthy):
```json
{
  "status": "unhealthy",
  "timestamp": "2026-02-09T12:00:00Z",
  "errors": [
    "Database connection failed",
    "SMTP configuration invalid"
  ]
}
```

**Status Codes**:
- `200 OK`: Application healthy
- `503 Service Unavailable`: Application unhealthy

**Checks**:
- Database connection is active
- SMTP configuration is valid
- All required environment variables are set
- Application is ready to accept requests

---

### Hugging Face Space Configuration

**File**: `README.md` (frontmatter)

**Required Frontmatter**:
```yaml
---
title: Todo Backend API
emoji: ✅
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
app_port: 8000
---
```

**Fields**:
- `title`: Space display name
- `emoji`: Space icon
- `colorFrom`, `colorTo`: Gradient colors for Space card
- `sdk`: Must be "docker" for Docker deployment
- `pinned`: Whether to pin Space to profile
- `app_port`: Port the application listens on (must match Dockerfile EXPOSE)

---

### Deployment Process (Backend)

**Steps**:
1. Push code to GitHub repository
2. Create new Space on Hugging Face
3. Select "Docker" as SDK
4. Connect GitHub repository to Space
5. Configure environment variables in Space settings
6. Space automatically builds Docker image
7. Space deploys container and runs health checks
8. Space provides public URL (e.g., `https://username-todo-backend.hf.space`)

**Build Time**: Target < 5 minutes

**Startup Time**: Target < 30 seconds

**Monitoring**:
- Check Space logs for build errors
- Monitor health check endpoint
- Verify API endpoints respond correctly
- Test CORS configuration with frontend

---

## Frontend Deployment (Vercel)

### Platform Requirements

**Platform**: Vercel
**Framework**: Next.js 16.1+
**Runtime**: Node.js 18.x or higher
**Deployment Method**: Git push to connected repository

### Build Configuration

**File**: `vercel.json` (optional)

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "framework": "nextjs",
  "installCommand": "npm install",
  "devCommand": "npm run dev"
}
```

**Build Settings** (Vercel Dashboard):
- Framework Preset: Next.js
- Build Command: `npm run build` (default)
- Output Directory: `.next` (default)
- Install Command: `npm install` (default)
- Node Version: 18.x

---

### Environment Variables (Frontend)

**Required Variables**:

| Variable | Type | Required | Secret | Description |
|----------|------|----------|--------|-------------|
| `NEXT_PUBLIC_API_URL` | string | Yes | No | Backend API URL (Hugging Face Space URL) |

**Format**:
```bash
NEXT_PUBLIC_API_URL=https://username-todo-backend.hf.space
```

**Important**:
- MUST use `NEXT_PUBLIC_` prefix for client-side variables
- MUST NOT include trailing slash
- MUST use HTTPS in production
- MUST match backend CORS configuration

**Configuration Location**:
- Vercel Dashboard → Project Settings → Environment Variables
- Set for "Production" environment
- Optionally set different values for "Preview" and "Development"

---

### Next.js Configuration

**File**: `frontend/next.config.ts`

**Production Settings**:
```typescript
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  reactStrictMode: true,
  poweredByHeader: false, // Remove X-Powered-By header

  // Environment variables validation
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },

  // Security headers
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
        ],
      },
    ];
  },
};

export default nextConfig;
```

---

### Deployment Process (Frontend)

**Steps**:
1. Push code to GitHub repository
2. Import project in Vercel dashboard
3. Select repository and branch (main)
4. Configure environment variables
5. Deploy (automatic on push to main branch)
6. Vercel provides public URL (e.g., `https://todo-app.vercel.app`)

**Build Time**: Target < 3 minutes

**Deployment Time**: Target < 1 minute

**Monitoring**:
- Check build logs for errors
- Verify deployment preview
- Test API connectivity to backend
- Verify authentication flow works

---

## CORS Configuration

### Backend CORS Settings

**Required Configuration**:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL")],  # Specific origin only
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,  # Cache preflight requests for 1 hour
)
```

**Security Requirements**:
- MUST use specific origin (not wildcard `*`)
- MUST set `allow_credentials=True` for cookie-based auth
- MUST restrict methods to only those used by application
- SHOULD cache preflight requests to reduce overhead

**Testing**:
- Verify OPTIONS preflight requests succeed
- Verify actual requests include CORS headers
- Verify credentials are sent with requests
- Verify unauthorized origins are blocked

---

## Security Headers

### Backend Security Headers

**Required Headers**:
```python
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response
```

### Frontend Security Headers

**Required Headers** (configured in `next.config.ts`):
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Referrer-Policy: strict-origin-when-cross-origin`

**Note**: Vercel automatically adds some security headers

---

## Logging Configuration

### Backend Logging

**Format**: JSON (structured logging)

**Example**:
```json
{
  "timestamp": "2026-02-09T12:00:00Z",
  "level": "INFO",
  "message": "Request processed",
  "method": "GET",
  "path": "/api/tasks",
  "status_code": 200,
  "duration_ms": 45,
  "user_id": "uuid-here",
  "correlation_id": "abc-123"
}
```

**Log Levels**:
- `DEBUG`: Detailed debugging information (development only)
- `INFO`: General informational messages (requests, responses)
- `WARNING`: Warning messages (rate limits, deprecated features)
- `ERROR`: Error messages (exceptions, failures)
- `CRITICAL`: Critical failures (startup errors, database failures)

**Production Settings**:
- Log Level: `INFO`
- Log Format: `json`
- Log Output: stdout (captured by platform)

**Security**:
- MUST NOT log passwords, tokens, or secrets
- MUST sanitize user input in logs
- MUST include correlation IDs for tracing
- SHOULD include user IDs for audit trail

---

## Monitoring and Alerting

### Health Checks

**Backend**:
- Endpoint: `GET /health`
- Interval: 30 seconds
- Timeout: 10 seconds
- Retries: 3

**Frontend**:
- Vercel automatic health checks
- Monitor build and deployment status

### Metrics

**Backend Metrics**:
- Request count by endpoint
- Response time by endpoint
- Error rate by endpoint
- Database connection pool usage
- Email sending success rate

**Frontend Metrics**:
- Build success rate
- Deployment time
- Page load time
- API request success rate

### Alerts

**Critical Alerts**:
- Health check failures (> 3 consecutive)
- Error rate > 5%
- Response time > 2 seconds (p95)
- Database connection failures

**Warning Alerts**:
- Error rate > 1%
- Response time > 1 second (p95)
- Email delivery failures > 10%

---

## Rollback Procedures

### Backend Rollback

**Steps**:
1. Identify failing deployment in Hugging Face Space logs
2. Revert to previous commit in GitHub
3. Space automatically rebuilds and deploys
4. Verify health checks pass
5. Monitor logs for errors

**Rollback Time**: Target < 10 minutes

### Frontend Rollback

**Steps**:
1. Go to Vercel dashboard → Deployments
2. Find previous successful deployment
3. Click "Promote to Production"
4. Verify deployment is live
5. Test critical user flows

**Rollback Time**: Target < 2 minutes (instant rollback)

---

## Disaster Recovery

### Database Backup

**Neon PostgreSQL**:
- Automatic daily backups (managed by Neon)
- Point-in-time recovery available
- Backup retention: 7 days (free tier)

**Recovery Process**:
1. Contact Neon support or use dashboard
2. Restore from backup to specific point in time
3. Update DATABASE_URL if new instance created
4. Redeploy backend with new connection string

### Configuration Backup

**Environment Variables**:
- Export environment variables from both platforms
- Store securely in password manager or secrets vault
- Document all required variables
- Test restoration process regularly

### Code Backup

**Git Repository**:
- Primary: GitHub repository
- Backup: Local clones on developer machines
- Tags: Create git tags for production releases
- Branches: Maintain stable main branch

---

## Performance Targets

### Backend

| Metric | Target | Measurement |
|--------|--------|-------------|
| Response Time (p50) | < 100ms | API endpoint latency |
| Response Time (p95) | < 500ms | API endpoint latency |
| Response Time (p99) | < 1000ms | API endpoint latency |
| Throughput | 100 req/s | Concurrent requests |
| Error Rate | < 1% | Failed requests / total |
| Uptime | 99.5% | Monthly availability |

### Frontend

| Metric | Target | Measurement |
|--------|--------|-------------|
| Build Time | < 3 min | Vercel build duration |
| Deployment Time | < 1 min | Vercel deployment duration |
| Page Load (p50) | < 1s | Time to interactive |
| Page Load (p95) | < 3s | Time to interactive |
| Uptime | 99.9% | Monthly availability |

---

## Cost Estimates

### Hugging Face Spaces (Free Tier)

**Included**:
- 2 vCPU
- 16GB RAM
- 50GB storage
- Unlimited bandwidth

**Limitations**:
- Cold start after inactivity
- Shared resources
- No SLA

**Upgrade Path**: Paid tiers available for dedicated resources

### Vercel (Hobby Tier)

**Included**:
- Unlimited deployments
- 100GB bandwidth/month
- Automatic HTTPS
- Global CDN

**Limitations**:
- 1 concurrent build
- 6000 build minutes/month
- No SLA

**Upgrade Path**: Pro tier for team features and higher limits

### Neon PostgreSQL (Free Tier)

**Included**:
- 0.5GB storage
- Unlimited queries
- Automatic backups (7 days)

**Limitations**:
- 1 project
- 10 branches
- No SLA

**Upgrade Path**: Paid tiers for more storage and features

---

## Compliance and Security

### Data Privacy

**GDPR Considerations**:
- User data stored in PostgreSQL (EU region if required)
- Email addresses used for authentication and password reset
- No tracking or analytics by default
- User can delete account and all data

### Security Compliance

**Best Practices**:
- HTTPS enforced on all platforms
- Secrets stored in platform environment variables
- Regular security updates for dependencies
- Input validation on all endpoints
- Rate limiting on authentication endpoints

### Audit Trail

**Logging**:
- All authentication events logged
- All password reset requests logged
- All API requests logged (without sensitive data)
- Logs retained for 30 days

---

## Testing Requirements

### Pre-Deployment Testing

**Backend**:
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Docker image builds successfully
- [ ] Health check endpoint responds
- [ ] Environment variables validated
- [ ] Database connection works
- [ ] SMTP connection works

**Frontend**:
- [ ] All unit tests pass
- [ ] Build completes without errors
- [ ] Environment variables configured
- [ ] API connectivity verified
- [ ] Authentication flow works

### Post-Deployment Testing

**Backend**:
- [ ] Health check returns 200 OK
- [ ] All API endpoints respond
- [ ] CORS headers present
- [ ] Security headers present
- [ ] Database queries work
- [ ] Email sending works

**Frontend**:
- [ ] Application loads successfully
- [ ] API requests succeed
- [ ] Authentication works
- [ ] All pages render correctly
- [ ] No console errors

---

## Documentation Requirements

**Required Documentation**:
- [ ] Deployment guide for Vercel (frontend)
- [ ] Deployment guide for Hugging Face (backend)
- [ ] Environment variables reference
- [ ] Troubleshooting guide
- [ ] Rollback procedures
- [ ] Monitoring and alerting setup

**Location**: `docs/deployment/`

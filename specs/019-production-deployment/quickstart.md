# Quickstart: Production Deployment

**Feature**: 019-production-deployment
**Date**: 2026-02-09
**Audience**: Developers and DevOps engineers

## Overview

This guide provides step-by-step instructions for deploying the Todo application to production with Docker containerization (backend on Hugging Face Spaces) and serverless deployment (frontend on Vercel).

**Prerequisites**:
- GitHub account with repository access
- Hugging Face account (free tier)
- Vercel account (free tier)
- Neon PostgreSQL database (already configured)
- SMTP service credentials (Gmail, SendGrid, or similar)

**Estimated Time**: 30-45 minutes

---

## Phase 1: Prepare Backend for Deployment

### Step 1: Create Dockerfile

**Location**: `backend/Dockerfile`

```dockerfile
# Multi-stage build for minimal image size
FROM python:3.13-slim as builder

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Runtime stage
FROM python:3.13-slim

WORKDIR /app

# Copy installed dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Set PATH to include user-installed packages
ENV PATH=/root/.local/bin:$PATH

# Expose application port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Run application with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Step 2: Create .dockerignore

**Location**: `backend/.dockerignore`

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
ENV/
*.egg-info/
dist/
build/

# Testing
.pytest_cache/
.coverage
htmlcov/
*.db
*.sqlite

# IDE
.vscode/
.idea/
*.swp
*.swo

# Git
.git/
.gitignore

# Documentation
*.md
docs/

# Environment
.env
.env.local
.env.*.local

# Logs
*.log
```

### Step 3: Update requirements.txt

Add email dependencies:

```bash
cd backend
echo "aiosmtplib==3.0.1" >> requirements.txt
```

### Step 4: Test Docker Build Locally

```bash
cd backend
docker build -t todo-backend .
docker run -p 8000:8000 \
  -e DATABASE_URL="your-neon-connection-string" \
  -e JWT_SECRET_KEY="your-secret-key-min-32-chars" \
  -e SMTP_HOST="smtp.gmail.com" \
  -e SMTP_PORT="587" \
  -e SMTP_USERNAME="your-email@gmail.com" \
  -e SMTP_PASSWORD="your-app-password" \
  -e SMTP_FROM_EMAIL="your-email@gmail.com" \
  -e FRONTEND_URL="http://localhost:3000" \
  todo-backend
```

**Verify**:
- Container starts without errors
- Health check passes: `curl http://localhost:8000/health`
- API responds: `curl http://localhost:8000/docs`

---

## Phase 2: Deploy Backend to Hugging Face Spaces

### Step 1: Create Hugging Face Space

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Fill in details:
   - **Space name**: `todo-backend` (or your preferred name)
   - **License**: Apache 2.0
   - **Select SDK**: Docker
   - **Space hardware**: CPU basic (free)
4. Click "Create Space"

### Step 2: Connect GitHub Repository

1. In your Space, go to "Settings" → "Repository"
2. Click "Connect to GitHub"
3. Select your repository
4. Choose branch: `main`
5. Set path to Dockerfile: `backend/Dockerfile`
6. Save settings

### Step 3: Configure Environment Variables

In Space Settings → Variables, add:

| Variable | Value | Secret |
|----------|-------|--------|
| `DATABASE_URL` | Your Neon connection string | ✓ |
| `JWT_SECRET_KEY` | Strong random string (32+ chars) | ✓ |
| `SMTP_HOST` | smtp.gmail.com (or your provider) | |
| `SMTP_PORT` | 587 | |
| `SMTP_USERNAME` | Your email address | |
| `SMTP_PASSWORD` | Your SMTP password/app password | ✓ |
| `SMTP_FROM_EMAIL` | Your sender email | |
| `SMTP_FROM_NAME` | Todo App | |
| `FRONTEND_URL` | https://your-app.vercel.app | |
| `ENVIRONMENT` | production | |

**Generate JWT Secret**:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 4: Add Space Configuration

**Location**: `backend/README.md` (add frontmatter at top)

```markdown
---
title: Todo Backend API
emoji: ✅
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
app_port: 8000
---

# Todo Backend API

Production backend for Todo application.

## API Documentation

Visit `/docs` for interactive API documentation.

## Health Check

Visit `/health` to check application status.
```

### Step 5: Deploy

1. Commit and push changes to GitHub:
   ```bash
   git add backend/Dockerfile backend/.dockerignore backend/README.md backend/requirements.txt
   git commit -m "feat: Add Docker configuration for production deployment"
   git push origin main
   ```

2. Hugging Face Space will automatically:
   - Pull latest code from GitHub
   - Build Docker image
   - Deploy container
   - Run health checks

3. Monitor build logs in Space interface

4. Once deployed, your backend will be available at:
   `https://YOUR-USERNAME-todo-backend.hf.space`

### Step 6: Verify Backend Deployment

```bash
# Replace with your Space URL
BACKEND_URL="https://YOUR-USERNAME-todo-backend.hf.space"

# Check health
curl $BACKEND_URL/health

# Check API docs
curl $BACKEND_URL/docs

# Test registration (optional)
curl -X POST $BACKEND_URL/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test1234!"}'
```

---

## Phase 3: Deploy Frontend to Vercel

### Step 1: Prepare Frontend Configuration

**Update**: `frontend/.env.example`

```bash
# Backend API URL (replace with your Hugging Face Space URL)
NEXT_PUBLIC_API_URL=https://YOUR-USERNAME-todo-backend.hf.space
```

### Step 2: Update Next.js Configuration

**File**: `frontend/next.config.ts`

Ensure security headers are configured:

```typescript
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,

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

### Step 3: Test Frontend Build Locally

```bash
cd frontend
npm install
npm run build
npm run start
```

Verify build completes without errors.

### Step 4: Deploy to Vercel

**Option A: Using Vercel Dashboard**

1. Go to https://vercel.com/new
2. Import your GitHub repository
3. Configure project:
   - **Framework Preset**: Next.js (auto-detected)
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (default)
   - **Output Directory**: `.next` (default)
4. Add environment variable:
   - **Name**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://YOUR-USERNAME-todo-backend.hf.space`
   - **Environment**: Production
5. Click "Deploy"

**Option B: Using Vercel CLI**

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy from frontend directory
cd frontend
vercel --prod

# Follow prompts to configure project
```

### Step 5: Configure Custom Domain (Optional)

1. In Vercel dashboard, go to Project Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions
4. Update `FRONTEND_URL` in backend environment variables

### Step 6: Verify Frontend Deployment

1. Visit your Vercel URL: `https://your-app.vercel.app`
2. Test user flows:
   - Register new account
   - Login
   - Create todo
   - Update todo
   - Delete todo
   - Logout
3. Test password reset:
   - Click "Forgot password"
   - Enter email
   - Check email for reset link
   - Reset password
   - Login with new password

---

## Phase 4: Update Backend CORS Configuration

After frontend is deployed, update backend CORS to use production URL:

1. Go to Hugging Face Space Settings → Variables
2. Update `FRONTEND_URL` to your Vercel URL:
   ```
   FRONTEND_URL=https://your-app.vercel.app
   ```
3. Space will automatically redeploy with new configuration

---

## Phase 5: Configure SMTP Email Service

### Option A: Gmail (Recommended for Testing)

1. Enable 2-factor authentication on your Google account
2. Generate App Password:
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Name it "Todo App"
   - Copy the generated password
3. Use these settings:
   - `SMTP_HOST`: smtp.gmail.com
   - `SMTP_PORT`: 587
   - `SMTP_USERNAME`: your-email@gmail.com
   - `SMTP_PASSWORD`: generated-app-password
   - `SMTP_FROM_EMAIL`: your-email@gmail.com

**Limitations**: 500 emails per day

### Option B: SendGrid (Recommended for Production)

1. Sign up at https://sendgrid.com (free tier: 100 emails/day)
2. Create API key:
   - Go to Settings → API Keys
   - Create API Key with "Mail Send" permissions
   - Copy the API key
3. Use these settings:
   - `SMTP_HOST`: smtp.sendgrid.net
   - `SMTP_PORT`: 587
   - `SMTP_USERNAME`: apikey
   - `SMTP_PASSWORD`: your-sendgrid-api-key
   - `SMTP_FROM_EMAIL`: verified-sender@yourdomain.com

**Note**: Verify sender email in SendGrid dashboard

### Option C: AWS SES (Recommended for Scale)

1. Sign up for AWS account
2. Verify email address or domain in SES
3. Create SMTP credentials in SES console
4. Use these settings:
   - `SMTP_HOST`: email-smtp.us-east-1.amazonaws.com (or your region)
   - `SMTP_PORT`: 587
   - `SMTP_USERNAME`: your-smtp-username
   - `SMTP_PASSWORD`: your-smtp-password
   - `SMTP_FROM_EMAIL`: verified@yourdomain.com

**Limitations**: Sandbox mode (200 emails/day) until production access requested

---

## Phase 6: Test Email Functionality

### Test Password Reset Email

1. Go to your frontend: `https://your-app.vercel.app`
2. Click "Forgot your password?"
3. Enter your email address
4. Click "Send Reset Link"
5. Check your email inbox
6. Click the reset link in email
7. Enter new password
8. Verify you can login with new password

### Troubleshooting Email Issues

**Email not received**:
- Check spam/junk folder
- Verify SMTP credentials are correct
- Check backend logs for email sending errors
- Verify sender email is verified (SendGrid, SES)
- Check SMTP provider rate limits

**Email delivery failed**:
- Check backend logs for SMTP errors
- Verify SMTP host and port are correct
- Verify TLS is enabled (port 587)
- Test SMTP connection manually:
  ```bash
  python -c "import smtplib; smtplib.SMTP('smtp.gmail.com', 587).starttls()"
  ```

---

## Phase 7: Monitoring and Maintenance

### Monitor Backend Health

**Hugging Face Space**:
- Check Space logs for errors
- Monitor health check endpoint
- Set up uptime monitoring (UptimeRobot, Pingdom)

**Health Check URL**:
```
https://YOUR-USERNAME-todo-backend.hf.space/health
```

### Monitor Frontend Performance

**Vercel Dashboard**:
- Check deployment status
- Monitor build times
- Review analytics (if enabled)
- Check error logs

### Database Monitoring

**Neon Dashboard**:
- Monitor connection count
- Check storage usage
- Review query performance
- Set up alerts for high usage

### Email Monitoring

**SMTP Provider Dashboard**:
- Monitor email delivery rate
- Check bounce rate
- Review spam complaints
- Monitor rate limit usage

---

## Rollback Procedures

### Rollback Backend

1. Go to Hugging Face Space
2. Check build logs for errors
3. Revert to previous commit in GitHub:
   ```bash
   git revert HEAD
   git push origin main
   ```
4. Space will automatically rebuild and deploy

### Rollback Frontend

1. Go to Vercel Dashboard → Deployments
2. Find previous successful deployment
3. Click "..." → "Promote to Production"
4. Deployment is instantly rolled back

---

## Security Checklist

Before going live, verify:

- [ ] All secrets are in environment variables (not in code)
- [ ] JWT secret is strong (32+ characters)
- [ ] SMTP password is secure (app password, not account password)
- [ ] Database connection uses SSL
- [ ] CORS is configured with specific origin (not wildcard)
- [ ] Security headers are enabled
- [ ] Rate limiting is enabled
- [ ] HTTPS is enforced on all platforms
- [ ] Error messages don't expose sensitive information
- [ ] Logs don't contain passwords or tokens

---

## Performance Optimization

### Backend Optimization

- Use connection pooling for database
- Enable response caching where appropriate
- Optimize database queries (add indexes)
- Monitor and optimize slow endpoints
- Consider adding Redis for session storage (future)

### Frontend Optimization

- Enable Next.js image optimization
- Use dynamic imports for large components
- Implement code splitting
- Enable Vercel Analytics for insights
- Optimize bundle size

---

## Cost Management

### Free Tier Limits

**Hugging Face Spaces (Free)**:
- 2 vCPU, 16GB RAM
- 50GB storage
- Unlimited bandwidth
- Cold start after inactivity

**Vercel (Hobby)**:
- 100GB bandwidth/month
- 6000 build minutes/month
- Unlimited deployments

**Neon (Free)**:
- 0.5GB storage
- Unlimited queries
- 7-day backups

**SMTP (Gmail)**:
- 500 emails/day

### Upgrade Triggers

Consider upgrading when:
- Backend needs dedicated resources (no cold starts)
- Frontend exceeds bandwidth limits
- Database exceeds storage limits
- Email volume exceeds free tier limits
- Need SLA guarantees

---

## Troubleshooting

### Common Issues

**Backend won't start**:
- Check environment variables are set correctly
- Verify DATABASE_URL is accessible from Hugging Face
- Check Dockerfile syntax
- Review build logs for errors

**Frontend can't reach backend**:
- Verify NEXT_PUBLIC_API_URL is correct
- Check CORS configuration in backend
- Verify backend is running (health check)
- Check browser console for CORS errors

**Email not sending**:
- Verify SMTP credentials
- Check SMTP host and port
- Verify sender email is verified
- Check rate limits
- Review backend logs

**Database connection failed**:
- Verify DATABASE_URL is correct
- Check Neon database is running
- Verify SSL mode is enabled
- Check connection pool settings

---

## Next Steps

After successful deployment:

1. **Set up monitoring**: Configure uptime monitoring and alerts
2. **Enable analytics**: Add Vercel Analytics or Google Analytics
3. **Configure backups**: Verify Neon backups are enabled
4. **Document runbooks**: Create operational procedures
5. **Plan scaling**: Monitor usage and plan for growth
6. **Security audit**: Regular security reviews and updates
7. **Performance testing**: Load test backend endpoints
8. **User feedback**: Collect and act on user feedback

---

## Support and Resources

**Documentation**:
- [Hugging Face Spaces Docs](https://huggingface.co/docs/hub/spaces)
- [Vercel Docs](https://vercel.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Next.js Deployment](https://nextjs.org/docs/deployment)

**Community**:
- Hugging Face Discord
- Vercel Discord
- FastAPI GitHub Discussions
- Next.js GitHub Discussions

**Monitoring Tools**:
- [UptimeRobot](https://uptimerobot.com) - Free uptime monitoring
- [Sentry](https://sentry.io) - Error tracking
- [LogRocket](https://logrocket.com) - Frontend monitoring

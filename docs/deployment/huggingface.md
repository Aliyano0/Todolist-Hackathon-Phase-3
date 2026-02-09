# Deploying Backend to Hugging Face Spaces

**Platform**: Hugging Face Spaces (Docker)
**Target**: Production deployment of Todo Backend API
**Prerequisites**: Hugging Face account, Git installed

---

## Overview

Hugging Face Spaces provides free Docker container hosting, perfect for deploying our FastAPI backend. This guide walks you through the complete deployment process.

---

## Step 1: Create Hugging Face Account

1. Go to [huggingface.co](https://huggingface.co)
2. Click "Sign Up" and create a free account
3. Verify your email address
4. Complete your profile

---

## Step 2: Create a New Space

1. Navigate to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Configure your Space:
   - **Space name**: `todo-backend` (or your preferred name)
   - **License**: Apache 2.0 (recommended)
   - **Select the Space SDK**: Docker
   - **Space hardware**: CPU basic (free tier)
   - **Visibility**: Public or Private (your choice)
4. Click "Create Space"

---

## Step 3: Prepare Your Repository

### Add README.md with Frontmatter

Create `backend/README.md` with Hugging Face Space configuration:

```markdown
---
title: Todo Backend API
emoji: 📝
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 8000
pinned: false
---

# Todo Backend API

FastAPI backend for Todo application with JWT authentication and email notifications.

## Features

- RESTful API with FastAPI
- JWT-based authentication
- Email-based password reset
- PostgreSQL database (Neon)
- Docker containerized
- Health check endpoint

## API Documentation

Once deployed, visit:
- Swagger UI: `https://your-space-url/docs`
- ReDoc: `https://your-space-url/redoc`
- Health Check: `https://your-space-url/health`

## Environment Variables

See deployment documentation for required environment variables.
```

### Verify Dockerfile

Ensure your `backend/Dockerfile` is ready:
- ✅ Exposes port 8000
- ✅ Has HEALTHCHECK instruction
- ✅ Uses environment variables
- ✅ Runs uvicorn with proper configuration

---

## Step 4: Configure Environment Variables

### Required Secrets

In your Hugging Face Space settings, add these secrets:

#### Database Configuration
```bash
DATABASE_URL=postgresql+asyncpg://user:password@host/database?sslmode=require
```
**Get this from**: Neon PostgreSQL (see neon-setup.md)

#### JWT Configuration
```bash
JWT_SECRET_KEY=<generate-32-character-random-string>
BETTER_AUTH_SECRET=<generate-32-character-random-string>
```
**Generate with**:
```bash
# On Linux/Mac
openssl rand -base64 32

# On Windows (PowerShell)
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))

# Or use online generator (for development only)
# https://generate-secret.vercel.app/32
```

#### SMTP Configuration
```bash 
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=<paji peyr ksts mjnt>
SMTP_FROM_EMAIL=noreply@yourdomain.com
SMTP_FROM_NAME=Todo App
SMTP_USE_TLS=true
```
**Get this from**: Gmail App Password or SendGrid (see smtp-setup.md)

#### Frontend Configuration
```bash
FRONTEND_URL=https://your-frontend.vercel.app
```
**Get this from**: Your Vercel deployment URL

#### Optional Configuration
```bash
ENVIRONMENT=production
PORT=8000
WORKERS=4
LOG_LEVEL=INFO
LOG_FORMAT=json
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60
```

### How to Add Secrets

1. Go to your Space settings
2. Click "Variables and secrets"
3. Click "New secret"
4. Add each variable:
   - Name: `DATABASE_URL`
   - Value: `postgresql+asyncpg://...`
   - Click "Save"
5. Repeat for all required variables

**Important**: Never commit secrets to Git!

---

## Step 5: Deploy to Hugging Face

### Option A: Deploy via Git (Recommended)

```bash
# 1. Clone your Space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/todo-backend
cd todo-backend

# 2. Copy backend files
cp -r /path/to/your/backend/* .

# 3. Ensure README.md has frontmatter
# (Should be at root of repository)

# 4. Commit and push
git add .
git commit -m "Initial deployment: Todo Backend API"
git push

# 5. Hugging Face will automatically build and deploy
```

### Option B: Deploy via Web Interface

1. Go to your Space page
2. Click "Files and versions"
3. Click "Add file" → "Upload files"
4. Upload all files from `backend/` directory:
   - Dockerfile
   - requirements.txt
   - main.py
   - All subdirectories (api/, core/, models/, etc.)
   - README.md (with frontmatter)
5. Click "Commit changes to main"

---

## Step 6: Monitor Deployment

### Check Build Logs

1. Go to your Space page
2. Click "Logs" tab
3. Watch the build process:
   - Docker image building
   - Dependencies installing
   - Container starting

**Expected build time**: 2-5 minutes

### Common Build Issues

**Issue**: `ModuleNotFoundError`
- **Cause**: Missing dependency in requirements.txt
- **Fix**: Add missing package and redeploy

**Issue**: `ValueError: DATABASE_URL must be set`
- **Cause**: Environment variable not configured
- **Fix**: Add secret in Space settings

**Issue**: `ConnectionRefusedError`
- **Cause**: Invalid database URL
- **Fix**: Verify Neon connection string

---

## Step 7: Verify Deployment

### Test Health Check

```bash
curl https://YOUR_USERNAME-todo-backend.hf.space/health
```

**Expected response**:
```json
{
  "status": "healthy",
  "timestamp": "2026-02-08T12:00:00Z",
  "version": "0.1.0",
  "database": "connected",
  "smtp": "configured"
}
```

### Test API Documentation

Visit: `https://YOUR_USERNAME-todo-backend.hf.space/docs`

You should see the Swagger UI with all API endpoints.

### Test Authentication

```bash
# Register a user
curl -X POST https://YOUR_USERNAME-todo-backend.hf.space/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123!"
  }'

# Expected: 201 Created with user data
```

---

## Step 8: Update Frontend Configuration

Update your frontend environment variables:

```bash
# frontend/.env.local
NEXT_PUBLIC_API_URL=https://YOUR_USERNAME-todo-backend.hf.space
```

Redeploy your frontend to Vercel.

---

## Troubleshooting

### Container Keeps Restarting

**Check logs for**:
- Database connection errors → Verify DATABASE_URL
- Missing environment variables → Add all required secrets
- Port binding issues → Ensure PORT=8000

### Health Check Fails

**Possible causes**:
1. Database not accessible → Check Neon connection
2. SMTP configuration invalid → Verify SMTP credentials
3. Application startup error → Check logs

### Slow Response Times

**Solutions**:
1. Upgrade to better hardware (paid tier)
2. Optimize database queries
3. Add caching layer
4. Use connection pooling

### CORS Errors

**Fix**: Ensure FRONTEND_URL matches your Vercel deployment:
```bash
FRONTEND_URL=https://your-app.vercel.app
```

---

## Monitoring & Maintenance

### Check Application Status

```bash
# Health check
curl https://YOUR_USERNAME-todo-backend.hf.space/health

# API status
curl https://YOUR_USERNAME-todo-backend.hf.space/
```

### View Logs

1. Go to Space page
2. Click "Logs" tab
3. Monitor for errors or warnings

### Update Deployment

```bash
# Make changes locally
git add .
git commit -m "Update: description of changes"
git push

# Hugging Face automatically rebuilds and redeploys
```

---

## Security Checklist

Before going live:

- [ ] All secrets configured (not in code)
- [ ] JWT_SECRET_KEY is strong (32+ characters)
- [ ] BETTER_AUTH_SECRET is strong (32+ characters)
- [ ] Database uses SSL (sslmode=require)
- [ ] SMTP credentials are secure (app password, not main password)
- [ ] FRONTEND_URL is correct (for CORS)
- [ ] Rate limiting enabled
- [ ] Logs don't expose sensitive data

---

## Cost Considerations

### Free Tier Limits

- **CPU**: Basic (free)
- **Memory**: 16GB RAM
- **Storage**: 50GB
- **Bandwidth**: Unlimited
- **Uptime**: May sleep after inactivity

### Upgrade Options

If you need more resources:
- **CPU Upgrade**: $0.60/hour for better performance
- **Persistent Storage**: For file uploads
- **Always-On**: Prevent sleeping

---

## Next Steps

1. ✅ Deploy backend to Hugging Face Spaces
2. ✅ Verify health check passes
3. ✅ Test API endpoints
4. 📝 Deploy frontend to Vercel (see vercel.md)
5. 🧪 Test end-to-end password reset flow
6. 📊 Set up monitoring and alerts

---

## Support & Resources

- **Hugging Face Docs**: https://huggingface.co/docs/hub/spaces
- **Docker Spaces Guide**: https://huggingface.co/docs/hub/spaces-sdks-docker
- **Community Forum**: https://discuss.huggingface.co/

---

## Quick Reference

### Space URL Format
```
https://YOUR_USERNAME-SPACE_NAME.hf.space
```

### API Endpoints
```
GET  /health              # Health check
GET  /docs                # Swagger UI
POST /api/auth/register   # Register user
POST /api/auth/login      # Login
POST /api/auth/password-reset/request  # Request reset
```

### Environment Variables
See `environment.md` for complete reference.

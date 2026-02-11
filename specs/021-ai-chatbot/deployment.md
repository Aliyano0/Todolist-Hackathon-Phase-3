# Deployment Guide: Phase III - AI Chatbot Integration

**Date**: 2026-02-10
**Feature**: [spec.md](./spec.md)
**Status**: Production Ready

## Overview

This guide provides step-by-step instructions for deploying the Todo application with AI chatbot integration to production environments.

**Deployment Architecture**:
- **Backend**: Hugging Face Spaces (Docker container)
- **Frontend**: Vercel (Next.js serverless)
- **Database**: Neon Serverless PostgreSQL
- **Email**: SendGrid (recommended) or SMTP provider
- **LLM**: OpenRouter API (gpt-4o-mini)

## Prerequisites

Before deploying, ensure you have:
- [ ] GitHub repository with latest code
- [ ] Neon PostgreSQL database created
- [ ] OpenRouter API account and API key
- [ ] SendGrid account and API key (or SMTP credentials)
- [ ] Hugging Face account
- [ ] Vercel account
- [ ] All environment variables documented

## Part 1: Database Setup (Neon PostgreSQL)

### 1.1 Create Neon Database

1. Go to [Neon Console](https://console.neon.tech/)
2. Click "Create Project"
3. Configure project:
   - **Name**: `todolist-production`
   - **Region**: Choose closest to your users (e.g., US East, EU West)
   - **Postgres Version**: 17 (latest)
4. Click "Create Project"

### 1.2 Get Connection String

1. In Neon dashboard, go to "Connection Details"
2. Copy the connection string (format: `postgresql://user:pass@host/db?sslmode=require`)
3. Convert to asyncpg format: `postgresql+asyncpg://user:pass@host/db`
4. Save for later use in environment variables

### 1.3 Run Database Migrations

```bash
# From your local machine with DATABASE_URL set
cd backend

# Activate virtual environment
source .venv/bin/activate

# Set DATABASE_URL
export DATABASE_URL="postgresql+asyncpg://user:pass@host/db"

# Run migrations
alembic upgrade head

# Verify tables created
psql $DATABASE_URL -c "\dt"

# Expected tables:
# - user
# - todotask
# - conversation
# - message
```

### 1.4 Verify Database Schema

```sql
-- Connect to database
psql $DATABASE_URL

-- Check user table
\d user

-- Check todotask table
\d todotask

-- Check conversation table
\d conversation

-- Check message table
\d message

-- Verify indexes exist
\di

-- Expected indexes:
-- - idx_conversation_user_id
-- - idx_message_conversation_id
-- - idx_message_created_at
```

## Part 2: Backend Deployment (Hugging Face Spaces)

### 2.1 Prepare Backend for Deployment

1. **Verify Dockerfile exists** at `backend/Dockerfile`
2. **Verify .dockerignore exists** at `backend/.dockerignore`
3. **Test Docker build locally**:

```bash
cd backend

# Build Docker image
docker build -t todolist-backend .

# Test locally
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql+asyncpg://..." \
  -e JWT_SECRET_KEY="your-secret-key" \
  -e OPENROUTER_API_KEY="sk-or-v1-..." \
  -e SENDGRID_API_KEY="SG...." \
  -e SENDGRID_FROM_EMAIL="noreply@example.com" \
  -e FRONTEND_URL="http://localhost:3000" \
  todolist-backend

# Test health endpoint
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","timestamp":"...","database":"connected","smtp":"configured"}
```

### 2.2 Create Hugging Face Space

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Configure Space:
   - **Owner**: Your username or organization
   - **Space name**: `todolist-backend`
   - **License**: MIT
   - **SDK**: Docker
   - **Visibility**: Public or Private
4. Click "Create Space"

### 2.3 Configure Space Settings

1. In Space settings, go to "Variables and secrets"
2. Add the following secrets (click "New secret"):

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host/db

# Authentication
JWT_SECRET_KEY=your-secret-key-minimum-32-characters-long
JWT_ALGORITHM=HS256

# OpenRouter API
OPENROUTER_API_KEY=sk-or-v1-your-openrouter-api-key-here

# Email Service (SendGrid recommended)
EMAIL_PROVIDER=sendgrid
SENDGRID_API_KEY=SG.your-sendgrid-api-key-here
SENDGRID_FROM_EMAIL=noreply@yourdomain.com
SENDGRID_FROM_NAME=Todo App

# Frontend URL (update after frontend deployment)
FRONTEND_URL=https://your-frontend.vercel.app

# Server Configuration
ENVIRONMENT=production
HOST=0.0.0.0
PORT=7860
WORKERS=4

# Security and Performance
RATE_LIMIT_ENABLED=true
LOG_LEVEL=INFO
```

**Important Notes**:
- Use PORT=7860 (Hugging Face Spaces default)
- Mark all secrets as "Secret" (not visible in logs)
- FRONTEND_URL will be updated after frontend deployment

### 2.4 Deploy Backend Code

**Option A: Git Push (Recommended)**

```bash
# Add Hugging Face remote
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/todolist-backend

# Push backend code
git subtree push --prefix backend hf main

# Or if you have the entire repo:
git push hf main
```

**Option B: Manual Upload**

1. In Space, click "Files and versions"
2. Upload the following files from `backend/`:
   - `Dockerfile`
   - `main.py`
   - `pyproject.toml`
   - All directories: `api/`, `core/`, `database/`, `models/`, `schemas/`, `dependencies/`, `mcp_server/`
3. Click "Commit changes to main"

### 2.5 Monitor Deployment

1. Go to "App" tab in Space
2. Watch build logs for errors
3. Wait for "Running" status (takes 2-5 minutes)
4. Test endpoints:

```bash
# Get Space URL (e.g., https://username-todolist-backend.hf.space)
BACKEND_URL="https://username-todolist-backend.hf.space"

# Test health endpoint
curl $BACKEND_URL/health

# Test root endpoint
curl $BACKEND_URL/

# Expected: {"status":"healthy","message":"Todo API is running","version":"0.1.0"}
```

### 2.6 Troubleshooting Backend Deployment

**Issue: Build fails with "No module named 'X'"**
- Solution: Verify all dependencies in `pyproject.toml`
- Check Docker build logs for missing packages

**Issue: Database connection fails**
- Solution: Verify DATABASE_URL format: `postgresql+asyncpg://...`
- Check Neon database is accessible (not paused)
- Verify SSL mode is correct

**Issue: Port binding error**
- Solution: Ensure PORT=7860 in environment variables
- Hugging Face Spaces requires port 7860

**Issue: CORS errors**
- Solution: Update FRONTEND_URL to match Vercel deployment URL
- Restart Space after updating environment variables

## Part 3: Frontend Deployment (Vercel)

### 3.1 Prepare Frontend for Deployment

1. **Verify next.config.ts** has production settings
2. **Test production build locally**:

```bash
cd frontend

# Install dependencies
npm install

# Build for production
npm run build

# Expected output: All 9 routes compiled successfully

# Test production server
npm run start

# Open http://localhost:3000 and verify:
# - Homepage loads
# - Login/Register work
# - Dashboard loads (after login)
# - Chat interface loads (after email verification)
```

### 3.2 Create Vercel Project

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New..." → "Project"
3. Import Git Repository:
   - Connect GitHub account if not connected
   - Select your repository
   - Click "Import"

### 3.3 Configure Vercel Project

1. **Framework Preset**: Next.js (auto-detected)
2. **Root Directory**: `frontend` (if monorepo) or `.` (if separate repo)
3. **Build Command**: `npm run build` (default)
4. **Output Directory**: `.next` (default)
5. **Install Command**: `npm install` (default)

### 3.4 Add Environment Variables

In Vercel project settings, go to "Environment Variables" and add:

```bash
# Backend API URL (use Hugging Face Space URL)
NEXT_PUBLIC_API_URL=https://username-todolist-backend.hf.space

# Better Auth Configuration
BETTER_AUTH_SECRET=your-secret-key-here-same-as-backend
BETTER_AUTH_URL=https://your-project.vercel.app

# Node Environment
NODE_ENV=production
```

**Important Notes**:
- `NEXT_PUBLIC_API_URL` must NOT have trailing slash
- `BETTER_AUTH_URL` will be auto-filled after first deployment
- Use same `BETTER_AUTH_SECRET` as backend JWT_SECRET_KEY

### 3.5 Deploy Frontend

1. Click "Deploy"
2. Wait for build to complete (2-3 minutes)
3. Vercel will provide a URL: `https://your-project.vercel.app`

### 3.6 Update Backend CORS Configuration

After frontend deployment, update backend environment variables:

1. Go to Hugging Face Space settings
2. Update `FRONTEND_URL` to Vercel URL: `https://your-project.vercel.app`
3. Restart Space (click "Factory reboot" in settings)

### 3.7 Update Frontend Environment Variables

1. Go to Vercel project settings → Environment Variables
2. Update `BETTER_AUTH_URL` to actual Vercel URL: `https://your-project.vercel.app`
3. Redeploy frontend (Vercel → Deployments → Redeploy)

### 3.8 Verify Frontend Deployment

```bash
# Get Vercel URL
FRONTEND_URL="https://your-project.vercel.app"

# Test homepage
curl $FRONTEND_URL

# Test API connectivity (should redirect to login)
curl -I $FRONTEND_URL/todos

# Open in browser and verify:
# - Homepage loads with animations
# - Login/Register forms work
# - Dashboard loads after login
# - Chat interface requires email verification
# - Email verification flow works
```

### 3.9 Troubleshooting Frontend Deployment

**Issue: Build fails with TypeScript errors**
- Solution: Run `npm run build` locally to catch errors
- Fix all type errors before deploying

**Issue: API requests fail with CORS errors**
- Solution: Verify FRONTEND_URL in backend matches Vercel URL exactly
- Check backend CORS middleware allows Vercel domain

**Issue: Authentication not working**
- Solution: Verify BETTER_AUTH_SECRET matches between frontend and backend
- Check cookies are being set (httpOnly, secure in production)

**Issue: Environment variables not updating**
- Solution: Redeploy after changing environment variables
- Clear Vercel cache: Settings → Clear Cache

## Part 4: Email Service Setup (SendGrid)

### 4.1 Create SendGrid Account

1. Go to [SendGrid](https://sendgrid.com/)
2. Sign up for free account (100 emails/day)
3. Verify your email address

### 4.2 Verify Sender Identity

1. In SendGrid dashboard, go to "Settings" → "Sender Authentication"
2. Click "Verify a Single Sender"
3. Fill in sender details:
   - **From Name**: Todo App
   - **From Email**: noreply@yourdomain.com (or your email)
   - **Reply To**: support@yourdomain.com
4. Click "Create"
5. Check your email and click verification link

### 4.3 Create API Key

1. Go to "Settings" → "API Keys"
2. Click "Create API Key"
3. Configure:
   - **Name**: `todolist-production`
   - **Permissions**: Full Access (or Mail Send only)
4. Click "Create & View"
5. Copy API key (starts with `SG.`)
6. Save securely (you won't see it again)

### 4.4 Update Backend Environment Variables

1. Go to Hugging Face Space settings
2. Update email configuration:
   ```bash
   EMAIL_PROVIDER=sendgrid
   SENDGRID_API_KEY=SG.your-api-key-here
   SENDGRID_FROM_EMAIL=noreply@yourdomain.com
   SENDGRID_FROM_NAME=Todo App
   ```
3. Restart Space

### 4.5 Test Email Sending

```bash
# Register a new user
curl -X POST $BACKEND_URL/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!",
    "name": "Test User"
  }'

# Check SendGrid dashboard for email activity
# Go to "Activity" → "Email Activity"
# Verify email was sent successfully
```

## Part 5: OpenRouter API Setup

### 5.1 Create OpenRouter Account

1. Go to [OpenRouter](https://openrouter.ai/)
2. Sign up with GitHub or email
3. Verify your email

### 5.2 Add Credits

1. Go to "Credits" in dashboard
2. Add credits (minimum $5 recommended)
3. Verify balance shows in dashboard

### 5.3 Create API Key

1. Go to "Keys" in dashboard
2. Click "Create Key"
3. Configure:
   - **Name**: `todolist-production`
   - **Permissions**: Default (all models)
4. Copy API key (starts with `sk-or-v1-`)
5. Save securely

### 5.4 Update Backend Environment Variables

1. Go to Hugging Face Space settings
2. Add/update:
   ```bash
   OPENROUTER_API_KEY=sk-or-v1-your-api-key-here
   ```
3. Restart Space

### 5.5 Test Chat Endpoint

```bash
# Register and login to get JWT token
# (See email verification test above)

# Send chat message
curl -X POST $BACKEND_URL/api/{user_id}/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "message": "Add task: buy groceries"
  }'

# Expected response:
# {
#   "conversation_id": "uuid",
#   "message": "I've added the task 'buy groceries' to your list.",
#   "timestamp": "2026-02-10T12:00:00Z"
# }
```

## Part 6: Post-Deployment Verification

### 6.1 End-to-End Testing Checklist

Test the complete user flow:

- [ ] **Homepage**: Loads with animations and CTAs
- [ ] **Registration**: User can register with email/password
- [ ] **Email Verification**: Verification email received and link works
- [ ] **Login**: User can login with credentials
- [ ] **Dashboard**: Todo list loads and displays correctly
- [ ] **Task CRUD**: Can create, read, update, delete tasks
- [ ] **Chat Access**: Unverified user sees verification prompt
- [ ] **Chat Interface**: Verified user can access chat
- [ ] **Natural Language**: Chat understands "add task: X"
- [ ] **Task Listing**: Chat can list tasks
- [ ] **Task Completion**: Chat can mark tasks complete
- [ ] **Task Deletion**: Chat can delete tasks with confirmation
- [ ] **Task Update**: Chat can update task details
- [ ] **Multilingual**: Chat works in English, Roman Urdu, Urdu
- [ ] **Conversation Persistence**: Chat history persists across sessions
- [ ] **Rate Limiting**: Excessive messages blocked (10/minute)
- [ ] **Error Handling**: Graceful error messages for failures

### 6.2 Performance Testing

```bash
# Test response times
time curl $BACKEND_URL/health
# Expected: < 200ms

time curl $BACKEND_URL/api/{user_id}/tasks \
  -H "Authorization: Bearer TOKEN"
# Expected: < 500ms

# Test chat response time
time curl -X POST $BACKEND_URL/api/{user_id}/chat \
  -H "Authorization: Bearer TOKEN" \
  -d '{"message":"list tasks"}'
# Expected: < 3s (depends on OpenRouter API)
```

### 6.3 Security Verification

- [ ] **HTTPS**: All URLs use HTTPS in production
- [ ] **CORS**: Only frontend domain allowed
- [ ] **JWT**: Tokens expire after 7 days
- [ ] **Rate Limiting**: Chat limited to 10 messages/minute
- [ ] **Email Verification**: Chat requires verified email
- [ ] **User Isolation**: Users can only access their own data
- [ ] **SQL Injection**: Parameterized queries used (SQLModel)
- [ ] **XSS**: Input sanitization in place
- [ ] **Secrets**: No secrets in code or logs

### 6.4 Monitoring Setup

**Backend Monitoring (Hugging Face Spaces)**:
1. Go to Space → Logs
2. Monitor for errors and warnings
3. Check resource usage (CPU, Memory)

**Frontend Monitoring (Vercel)**:
1. Go to Project → Analytics
2. Monitor page views and performance
3. Check for errors in Real-time logs

**Database Monitoring (Neon)**:
1. Go to Project → Monitoring
2. Check connection count and query performance
3. Set up alerts for high usage

**Email Monitoring (SendGrid)**:
1. Go to Activity → Email Activity
2. Monitor delivery rates and bounces
3. Set up alerts for failures

**LLM Monitoring (OpenRouter)**:
1. Go to Dashboard → Usage
2. Monitor API calls and costs
3. Set up budget alerts

## Part 7: Maintenance and Updates

### 7.1 Updating Backend

```bash
# Make changes locally
cd backend
# ... edit files ...

# Test locally
docker build -t todolist-backend .
docker run -p 8000:8000 todolist-backend

# Push to Hugging Face
git add .
git commit -m "Update: description"
git push hf main

# Monitor deployment in Space logs
```

### 7.2 Updating Frontend

```bash
# Make changes locally
cd frontend
# ... edit files ...

# Test locally
npm run build
npm run start

# Push to GitHub (Vercel auto-deploys)
git add .
git commit -m "Update: description"
git push origin main

# Monitor deployment in Vercel dashboard
```

### 7.3 Database Migrations

```bash
# Create new migration
cd backend
alembic revision -m "description"

# Edit migration file in alembic/versions/

# Test locally
alembic upgrade head

# Deploy to production
# 1. Push code to Hugging Face
# 2. Run migration via Space terminal or locally with production DATABASE_URL
```

### 7.4 Rollback Procedures

**Backend Rollback**:
1. Go to Hugging Face Space → Files and versions
2. Click on previous commit
3. Click "Restore this version"

**Frontend Rollback**:
1. Go to Vercel → Deployments
2. Find previous successful deployment
3. Click "..." → "Promote to Production"

**Database Rollback**:
```bash
# Rollback one migration
alembic downgrade -1

# Rollback to specific version
alembic downgrade <revision_id>
```

## Part 8: Cost Estimation

### Monthly Costs (Estimated)

**Neon PostgreSQL**:
- Free tier: 0.5 GB storage, 1 compute unit
- Paid tier: $19/month for 10 GB storage
- **Estimated**: $0-19/month

**Hugging Face Spaces**:
- Free tier: 2 vCPU, 16 GB RAM, 50 GB storage
- Paid tier: $0.60/hour for upgraded hardware
- **Estimated**: $0/month (free tier sufficient)

**Vercel**:
- Free tier: 100 GB bandwidth, unlimited deployments
- Paid tier: $20/month for Pro features
- **Estimated**: $0/month (free tier sufficient)

**SendGrid**:
- Free tier: 100 emails/day
- Paid tier: $19.95/month for 50,000 emails
- **Estimated**: $0/month (free tier sufficient for MVP)

**OpenRouter API**:
- gpt-4o-mini: $0.15 per 1M input tokens, $0.60 per 1M output tokens
- Average chat: ~500 input + 200 output tokens = $0.0002 per message
- 1000 messages/month: ~$0.20
- **Estimated**: $1-5/month

**Total Estimated Cost**: $1-24/month (depending on usage)

## Part 9: Production Checklist

Before going live, verify:

### Backend
- [ ] All environment variables set correctly
- [ ] Database migrations run successfully
- [ ] Health endpoint returns 200 OK
- [ ] CORS configured for frontend domain
- [ ] Rate limiting enabled
- [ ] Logging configured (JSON format)
- [ ] Error handling tested
- [ ] Security headers present

### Frontend
- [ ] Production build succeeds
- [ ] All routes accessible
- [ ] API connectivity verified
- [ ] Authentication flow works
- [ ] Email verification flow works
- [ ] Chat interface functional
- [ ] Responsive design verified
- [ ] Accessibility audit passed

### Database
- [ ] All tables created
- [ ] Indexes created
- [ ] Backup strategy in place
- [ ] Connection pooling configured

### Email
- [ ] Sender identity verified
- [ ] API key configured
- [ ] Test email sent successfully
- [ ] Email templates tested

### LLM
- [ ] API key configured
- [ ] Credits added to account
- [ ] Test chat message successful
- [ ] Budget alerts configured

### Monitoring
- [ ] Backend logs accessible
- [ ] Frontend analytics enabled
- [ ] Database monitoring active
- [ ] Email delivery tracking enabled
- [ ] LLM usage tracking enabled

## Part 10: Support and Resources

### Documentation
- [Hugging Face Spaces Docs](https://huggingface.co/docs/hub/spaces)
- [Vercel Docs](https://vercel.com/docs)
- [Neon Docs](https://neon.tech/docs)
- [SendGrid Docs](https://docs.sendgrid.com/)
- [OpenRouter Docs](https://openrouter.ai/docs)

### Troubleshooting
- Check backend logs in Hugging Face Space
- Check frontend logs in Vercel dashboard
- Check database logs in Neon console
- Check email activity in SendGrid dashboard
- Check LLM usage in OpenRouter dashboard

### Getting Help
- GitHub Issues: Report bugs and feature requests
- Community: Join Discord/Slack for support
- Documentation: Review project docs and CLAUDE.md files

## Conclusion

Your Todo application with AI chatbot is now deployed to production! Users can:
- Register and verify their email
- Manage tasks via traditional UI
- Interact with AI chatbot for natural language task management
- Access the app from anywhere with internet connection

Monitor usage, gather feedback, and iterate based on user needs.

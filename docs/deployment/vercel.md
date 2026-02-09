# Deploying Frontend to Vercel

**Platform**: Vercel (Next.js Serverless)
**Target**: Production deployment of Todo Frontend
**Prerequisites**: Vercel account, Git installed

---

## Overview

Vercel is the optimal platform for Next.js applications, providing automatic deployments, edge functions, and global CDN. This guide walks you through deploying your Todo frontend.

---

## Step 1: Create Vercel Account

1. Go to [vercel.com](https://vercel.com)
2. Click "Sign Up"
3. Choose sign-up method:
   - **GitHub** (recommended for automatic deployments)
   - **GitLab**
   - **Bitbucket**
   - **Email**
4. Complete account setup

---

## Step 2: Prepare Your Frontend

### Verify Next.js Configuration

Ensure `frontend/next.config.ts` is production-ready:

```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Disable powered by header for security
  poweredByHeader: false,

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

### Create Environment Variables Template

Create `frontend/.env.example`:

```bash
# Backend API URL (required)
NEXT_PUBLIC_API_URL=https://your-backend.hf.space

# Better Auth Configuration (if using Better Auth)
BETTER_AUTH_SECRET=your-secret-here
BETTER_AUTH_URL=https://your-app.vercel.app
```

### Verify Build Works Locally

```bash
cd frontend

# Install dependencies
npm install

# Build for production
npm run build

# Test production build
npm start
```

**Expected**: Build completes without errors, app runs on http://localhost:3000

---

## Step 3: Deploy to Vercel

### Option A: Deploy via Vercel CLI (Recommended)

```bash
# 1. Install Vercel CLI
npm install -g vercel

# 2. Login to Vercel
vercel login

# 3. Navigate to frontend directory
cd frontend

# 4. Deploy
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? todo-frontend (or your choice)
# - Directory? ./ (current directory)
# - Override settings? No

# 5. Deploy to production
vercel --prod
```

### Option B: Deploy via GitHub (Automatic Deployments)

```bash
# 1. Push your code to GitHub
git add .
git commit -m "feat: Add frontend for deployment"
git push origin main

# 2. Go to vercel.com/new
# 3. Click "Import Project"
# 4. Select your GitHub repository
# 5. Configure project:
#    - Framework Preset: Next.js
#    - Root Directory: frontend
#    - Build Command: npm run build
#    - Output Directory: .next
# 6. Click "Deploy"
```

### Option C: Deploy via Vercel Dashboard

1. Go to [vercel.com/new](https://vercel.com/new)
2. Click "Add New..." → "Project"
3. Import your Git repository or upload files
4. Configure:
   - **Framework**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
5. Click "Deploy"

---

## Step 4: Configure Environment Variables

### Add Production Environment Variables

1. Go to your project dashboard on Vercel
2. Click "Settings" → "Environment Variables"
3. Add the following variables:

#### Required Variables

```bash
# Backend API URL (from Hugging Face deployment)
NEXT_PUBLIC_API_URL=https://YOUR_USERNAME-todo-backend.hf.space
```

#### Optional Variables (if using Better Auth)

```bash
# Better Auth Secret (32+ characters)
BETTER_AUTH_SECRET=<generate-random-32-char-string>

# Better Auth URL (your Vercel deployment URL)
BETTER_AUTH_URL=https://your-app.vercel.app
```

### Generate Secrets

```bash
# On Linux/Mac
openssl rand -base64 32

# On Windows (PowerShell)
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))
```

### Apply to All Environments

For each variable:
- Check: ✅ Production
- Check: ✅ Preview
- Check: ✅ Development

Click "Save" for each variable.

---

## Step 5: Redeploy with Environment Variables

After adding environment variables:

```bash
# Via CLI
vercel --prod

# Or via Dashboard
# Go to Deployments → Click "..." → "Redeploy"
```

---

## Step 6: Configure Custom Domain (Optional)

### Add Custom Domain

1. Go to project "Settings" → "Domains"
2. Click "Add"
3. Enter your domain: `yourdomain.com`
4. Follow DNS configuration instructions:

**For Vercel DNS**:
- Vercel automatically configures

**For External DNS** (Cloudflare, GoDaddy, etc.):
- Add A record: `76.76.21.21`
- Add CNAME record: `cname.vercel-dns.com`

5. Wait for DNS propagation (5-60 minutes)

### Configure SSL

Vercel automatically provisions SSL certificates via Let's Encrypt.

---

## Step 7: Update Backend CORS

Update your backend environment variables on Hugging Face:

```bash
FRONTEND_URL=https://your-app.vercel.app
# Or if using custom domain:
FRONTEND_URL=https://yourdomain.com
```

Redeploy backend for changes to take effect.

---

## Step 8: Verify Deployment

### Test Frontend

1. Visit your deployment URL: `https://your-app.vercel.app`
2. Verify:
   - ✅ Page loads correctly
   - ✅ No console errors
   - ✅ Styles render properly
   - ✅ Images load

### Test API Connection

1. Open browser DevTools (F12)
2. Go to Network tab
3. Try to register/login
4. Verify:
   - ✅ API requests go to correct backend URL
   - ✅ No CORS errors
   - ✅ Responses return successfully

### Test Authentication Flow

```bash
# 1. Register new user
# 2. Login with credentials
# 3. Create a todo
# 4. Logout
# 5. Request password reset
# 6. Check email for reset link
# 7. Reset password
# 8. Login with new password
```

---

## Step 9: Configure Production Settings

### Enable Analytics (Optional)

1. Go to "Analytics" tab
2. Enable Vercel Analytics
3. View real-time traffic and performance

### Enable Speed Insights (Optional)

1. Go to "Speed Insights" tab
2. Enable Speed Insights
3. Monitor Core Web Vitals

### Configure Deployment Protection

1. Go to "Settings" → "Deployment Protection"
2. Enable:
   - ✅ Vercel Authentication (for preview deployments)
   - ✅ Password Protection (optional)

---

## Troubleshooting

### Build Fails

**Check build logs for**:
- Missing dependencies → Run `npm install` locally
- TypeScript errors → Fix type issues
- Environment variables → Ensure NEXT_PUBLIC_* variables are set

**Common fixes**:
```bash
# Clear cache and rebuild
rm -rf .next node_modules
npm install
npm run build
```

### API Connection Fails

**Symptoms**: Network errors, CORS errors

**Fixes**:
1. Verify `NEXT_PUBLIC_API_URL` is correct
2. Check backend CORS configuration
3. Ensure backend `FRONTEND_URL` matches Vercel URL
4. Check browser console for specific errors

### Environment Variables Not Working

**Issue**: Variables undefined in code

**Cause**: Variables must start with `NEXT_PUBLIC_` to be exposed to browser

**Fix**:
```bash
# ❌ Wrong
API_URL=https://backend.com

# ✅ Correct
NEXT_PUBLIC_API_URL=https://backend.com
```

### Slow Page Loads

**Solutions**:
1. Enable Image Optimization
2. Use Next.js Image component
3. Implement code splitting
4. Enable caching headers

---

## Automatic Deployments

### GitHub Integration

Once connected to GitHub:
- **Push to main** → Automatic production deployment
- **Push to branch** → Automatic preview deployment
- **Pull request** → Preview deployment with unique URL

### Preview Deployments

Every branch/PR gets a unique URL:
```
https://your-app-git-feature-branch-username.vercel.app
```

Share preview URLs for testing before merging.

---

## Monitoring & Performance

### View Deployment Logs

1. Go to "Deployments" tab
2. Click on a deployment
3. View:
   - Build logs
   - Function logs
   - Runtime logs

### Monitor Performance

1. Go to "Analytics" tab
2. View metrics:
   - Page views
   - Unique visitors
   - Top pages
   - Referrers

### Check Speed Insights

1. Go to "Speed Insights" tab
2. Monitor Core Web Vitals:
   - LCP (Largest Contentful Paint)
   - FID (First Input Delay)
   - CLS (Cumulative Layout Shift)

---

## Security Best Practices

### Environment Variables

- [ ] Never commit `.env.local` to Git
- [ ] Use `NEXT_PUBLIC_` prefix only for client-side variables
- [ ] Keep secrets server-side only
- [ ] Rotate secrets regularly

### Security Headers

Verify headers are set (check in DevTools → Network):
- ✅ X-Content-Type-Options: nosniff
- ✅ X-Frame-Options: DENY
- ✅ X-XSS-Protection: 1; mode=block
- ✅ Referrer-Policy: strict-origin-when-cross-origin

### HTTPS

- ✅ Vercel automatically enforces HTTPS
- ✅ HTTP requests redirect to HTTPS
- ✅ SSL certificates auto-renewed

---

## Cost Considerations

### Free Tier (Hobby)

- **Bandwidth**: 100GB/month
- **Build Minutes**: 6,000 minutes/month
- **Serverless Functions**: 100GB-hours
- **Edge Functions**: 500,000 invocations
- **Domains**: Unlimited
- **Team Members**: 1

### Pro Tier ($20/month)

- **Bandwidth**: 1TB/month
- **Build Minutes**: 24,000 minutes/month
- **Serverless Functions**: 1,000GB-hours
- **Edge Functions**: 1,000,000 invocations
- **Team Members**: Unlimited
- **Advanced Analytics**: Included

---

## Rollback Deployments

### Instant Rollback

1. Go to "Deployments" tab
2. Find previous working deployment
3. Click "..." → "Promote to Production"
4. Confirm rollback

**Effect**: Instant switch to previous version (no rebuild needed)

---

## CI/CD Integration

### GitHub Actions (Optional)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Vercel
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
          vercel-args: '--prod'
```

---

## Next Steps

1. ✅ Deploy frontend to Vercel
2. ✅ Configure environment variables
3. ✅ Verify API connection
4. ✅ Test authentication flow
5. 🧪 Test password reset email flow
6. 📊 Set up monitoring
7. 🔒 Review security checklist

---

## Support & Resources

- **Vercel Docs**: https://vercel.com/docs
- **Next.js Docs**: https://nextjs.org/docs
- **Community**: https://github.com/vercel/vercel/discussions

---

## Quick Reference

### Deployment URL Format
```
https://PROJECT_NAME-USERNAME.vercel.app
```

### CLI Commands
```bash
vercel          # Deploy to preview
vercel --prod   # Deploy to production
vercel logs     # View logs
vercel env      # Manage environment variables
vercel domains  # Manage domains
```

### Environment Variables
```bash
NEXT_PUBLIC_API_URL=https://backend-url.hf.space
BETTER_AUTH_SECRET=<32-char-secret>
BETTER_AUTH_URL=https://your-app.vercel.app
```

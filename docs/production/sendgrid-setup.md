# SendGrid Email Service Setup Guide

## Problem: SMTP Port Blocked on Hugging Face Spaces

Hugging Face Spaces blocks outbound SMTP connections on ports 25, 465, and 587 for security reasons. This prevents the Gmail SMTP email service from working in production.

**Solution:** Use SendGrid API instead of SMTP. SendGrid uses HTTPS (port 443) which is not blocked.

---

## SendGrid Setup (5 minutes)

### Step 1: Create SendGrid Account

1. Go to https://sendgrid.com/
2. Click "Start for Free"
3. Sign up with your email
4. **Free Tier:** 100 emails/day (perfect for password resets)

### Step 2: Verify Sender Email

**IMPORTANT:** SendGrid requires sender verification to prevent spam.

1. Log in to SendGrid dashboard
2. Go to **Settings** → **Sender Authentication**
3. Click **Verify a Single Sender**
4. Fill in the form:
   - **From Name:** Todo App
   - **From Email Address:** Your email (e.g., aliyan119988@gmail.com)
   - **Reply To:** Same as from email
   - **Company Address:** Your address
5. Click **Create**
6. Check your email and click the verification link
7. Wait for "Verified" status in dashboard

### Step 3: Create API Key

1. Go to **Settings** → **API Keys**
2. Click **Create API Key**
3. Name: `Todo App Production`
4. Permissions: **Full Access** (or **Mail Send** only)
5. Click **Create & View**
6. **COPY THE API KEY NOW** (you won't see it again!)
   - Format: `SG.xxxxxxxxxxxxxxxxxx.yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy`

### Step 4: Configure Hugging Face Spaces

1. Go to https://huggingface.co/spaces/Aliyan-q/Todo-backend
2. Click **Settings** tab
3. Scroll to **Variables and secrets**
4. Add these environment variables:

```bash
# SendGrid Configuration (REQUIRED)
SENDGRID_API_KEY=SG.your-api-key-here
SENDGRID_FROM_EMAIL=aliyan119988@gmail.com  # Must match verified sender
SENDGRID_FROM_NAME=Todo App

# Email Provider Selection (REQUIRED)
EMAIL_PROVIDER=sendgrid
```

5. Click **Save**
6. Space will automatically restart (~30 seconds)

### Step 5: Verify Email Service

After restart, check the health endpoint:

```bash
curl https://aliyan-q-todo-backend.hf.space/health
```

Expected response:
```json
{
  "status": "healthy",
  "smtp": "configured"  // This checks email service is initialized
}
```

Check the logs for:
```
Email service initialized: SendGrid
```

### Step 6: Test Password Reset

1. Go to your frontend: https://todo-hackathon-one.vercel.app
2. Click "Forgot Password?"
3. Enter your email
4. Check your inbox for password reset email
5. Should arrive within 30 seconds

---

## Environment Variables Reference

### Required for SendGrid

```bash
SENDGRID_API_KEY=SG.your-api-key-here
SENDGRID_FROM_EMAIL=your-verified-email@example.com
EMAIL_PROVIDER=sendgrid
```

### Optional

```bash
SENDGRID_FROM_NAME=Todo App  # Default: "Todo App"
```

### Keep Existing Variables

```bash
# These remain unchanged
DATABASE_URL=postgresql+asyncpg://...
JWT_SECRET_KEY=your-secret-key
FRONTEND_URL=https://todo-hackathon-one.vercel.app

# SMTP variables can stay (will be ignored when using SendGrid)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=...
SMTP_PASSWORD=...
SMTP_FROM_EMAIL=...
```

---

## How It Works

### Email Provider Selection

The backend automatically chooses the email provider:

1. **SendGrid** (preferred): If `SENDGRID_API_KEY` is set
2. **SMTP** (fallback): If SMTP credentials are set
3. **None**: Logs warning if neither is configured

### SendGrid vs SMTP

| Feature | SendGrid | SMTP (Gmail) |
|---------|----------|--------------|
| **Works on HF Spaces** | ✅ Yes | ❌ No (port blocked) |
| **Setup Complexity** | Easy (API key) | Medium (app password) |
| **Free Tier** | 100 emails/day | Unlimited |
| **Delivery Speed** | Fast (~1-2s) | Fast (~1-2s) |
| **Reliability** | High | High |
| **Port Used** | 443 (HTTPS) | 587 (SMTP) |

---

## Troubleshooting

### Error: "SendGrid API error: 403"

**Cause:** Sender email not verified

**Fix:**
1. Go to SendGrid → Settings → Sender Authentication
2. Verify your sender email
3. Wait for "Verified" status
4. Ensure `SENDGRID_FROM_EMAIL` matches verified email exactly

### Error: "SendGrid API error: 401"

**Cause:** Invalid API key

**Fix:**
1. Check `SENDGRID_API_KEY` is correct (starts with `SG.`)
2. Ensure no extra spaces or quotes
3. Create a new API key if needed

### Email Not Received

**Check:**
1. Spam folder
2. SendGrid dashboard → Activity Feed (shows all sent emails)
3. Backend logs for errors
4. Sender email is verified

### Health Check Shows "smtp": "not_configured"

**Cause:** Email service failed to initialize

**Fix:**
1. Check Hugging Face Spaces logs for errors
2. Verify `SENDGRID_API_KEY` is set
3. Verify `EMAIL_PROVIDER=sendgrid` is set
4. Restart the space

---

## Testing Locally

To test SendGrid locally before deploying:

1. Add to `backend/.env`:
```bash
SENDGRID_API_KEY=SG.your-api-key-here
SENDGRID_FROM_EMAIL=your-verified-email@example.com
EMAIL_PROVIDER=sendgrid
```

2. Install httpx:
```bash
cd backend
pip install httpx==0.27.0
```

3. Run backend:
```bash
python main.py
```

4. Check logs for:
```
Email service initialized: SendGrid
```

5. Test password reset from frontend

---

## Cost & Limits

### SendGrid Free Tier
- **100 emails/day** (3,000/month)
- Perfect for password resets
- No credit card required
- Upgrade available if needed

### Typical Usage
- Password reset: 1 email per request
- 100 emails/day = ~100 password resets/day
- More than enough for most applications

---

## Migration from SMTP

No code changes needed! The backend automatically detects SendGrid configuration and uses it instead of SMTP.

**Steps:**
1. Set up SendGrid (above)
2. Add `SENDGRID_API_KEY` to Hugging Face
3. Add `EMAIL_PROVIDER=sendgrid`
4. Keep SMTP variables (they'll be ignored)
5. Restart space

---

## Security Notes

- ✅ API key stored in environment variables (not in code)
- ✅ Sender email must be verified (prevents spam)
- ✅ HTTPS encryption for all API calls
- ✅ Email addresses masked in logs
- ✅ No sensitive data in email templates

---

## Support

### SendGrid Documentation
- Getting Started: https://docs.sendgrid.com/for-developers/sending-email/api-getting-started
- API Reference: https://docs.sendgrid.com/api-reference/mail-send/mail-send

### SendGrid Dashboard
- Activity Feed: See all sent emails
- Statistics: Track delivery rates
- Suppressions: Manage bounces/spam reports

---

## Summary

1. ✅ Sign up for SendGrid (free)
2. ✅ Verify sender email
3. ✅ Create API key
4. ✅ Add to Hugging Face Spaces environment variables
5. ✅ Restart space
6. ✅ Test password reset

**Time:** ~5 minutes
**Cost:** Free (100 emails/day)
**Result:** Working email service on Hugging Face Spaces

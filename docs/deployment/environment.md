# Environment Variables Reference

**Complete reference for all environment variables used in the Todo application**

---

## Overview

This document provides a comprehensive reference for all environment variables required for production deployment of both backend and frontend.

---

## Backend Environment Variables

### Required Variables

These variables **must** be set for the application to start:

#### Database Configuration

```bash
DATABASE_URL=postgresql+asyncpg://user:password@host:port/database?sslmode=require
```

**Description**: PostgreSQL database connection string with asyncpg driver

**Format**: `postgresql+asyncpg://[user]:[password]@[host]:[port]/[database]?sslmode=require`

**Example** (Neon):
```bash
DATABASE_URL=postgresql+asyncpg://user:pass@ep-cool-darkness-123456.us-east-1.aws.neon.tech/neondb?sslmode=require
```

**Notes**:
- Must use `postgresql+asyncpg://` prefix (not `postgresql://`)
- Include `?sslmode=require` for secure connections
- Get from Neon dashboard connection string

---

#### JWT Configuration

```bash
JWT_SECRET_KEY=<minimum-32-characters-random-string>
```

**Description**: Secret key for signing JWT tokens

**Requirements**:
- Minimum 32 characters
- Cryptographically random
- Never commit to Git

**Generate**:
```bash
# Linux/Mac
openssl rand -base64 32

# Windows PowerShell
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))
```

**Example**:
```bash
JWT_SECRET_KEY=dGhpc2lzYXZlcnlzZWN1cmVzZWNyZXRrZXkxMjM0NTY3ODk=
```

---

```bash
BETTER_AUTH_SECRET=<minimum-32-characters-random-string>
```

**Description**: Secret key for Better Auth JWT verification

**Requirements**: Same as JWT_SECRET_KEY

**Generate**: Same method as JWT_SECRET_KEY

**Example**:
```bash
BETTER_AUTH_SECRET=YW5vdGhlcnNlY3VyZXNlY3JldGtleWZvcmF1dGhlbnRpY2F0aW9u
```

---

#### SMTP Configuration

```bash
SMTP_HOST=smtp.gmail.com
```

**Description**: SMTP server hostname

**Common values**:
- Gmail: `smtp.gmail.com`
- SendGrid: `smtp.sendgrid.net`
- AWS SES: `email-smtp.us-east-1.amazonaws.com`
- Mailgun: `smtp.mailgun.org`

---

```bash
SMTP_PORT=587
```

**Description**: SMTP server port

**Common values**:
- `587` - TLS/STARTTLS (recommended)
- `465` - SSL
- `25` - Unencrypted (not recommended)

**Default**: `587`

---

```bash
SMTP_USERNAME=your-email@gmail.com
```

**Description**: SMTP authentication username

**Format**: Usually your email address or API key

**Examples**:
- Gmail: `your-email@gmail.com`
- SendGrid: `apikey` (literal string)
- AWS SES: Your SMTP username from AWS

---

```bash
SMTP_PASSWORD=<your-smtp-password>
```

**Description**: SMTP authentication password

**Security**:
- Gmail: Use App Password (not main password)
- SendGrid: Use API key
- AWS SES: Use SMTP password from AWS

**Never**: Commit to Git or share publicly

---

```bash
SMTP_FROM_EMAIL=noreply@yourdomain.com
```

**Description**: Sender email address for outgoing emails

**Format**: Valid email address

**Best practices**:
- Use `noreply@` for transactional emails
- Use verified domain
- Match SMTP_USERNAME domain (for some providers)

**Example**:
```bash
SMTP_FROM_EMAIL=noreply@todoapp.com
```

---

```bash
SMTP_FROM_NAME=Todo App
```

**Description**: Sender name displayed in email clients

**Format**: Plain text string

**Example**:
```bash
SMTP_FROM_NAME=Todo App
```

**Default**: `Todo App`

---

#### Frontend Configuration

```bash
FRONTEND_URL=https://your-app.vercel.app
```

**Description**: Frontend application URL for CORS and email links

**Format**: Full URL with protocol (https://)

**Used for**:
- CORS allowed origins
- Password reset email links
- Redirect URLs

**Examples**:
```bash
# Vercel deployment
FRONTEND_URL=https://todo-app.vercel.app

# Custom domain
FRONTEND_URL=https://todoapp.com

# Development
FRONTEND_URL=http://localhost:3000
```

---

### Optional Variables (with defaults)

These variables have sensible defaults but can be customized:

#### Application Configuration

```bash
ENVIRONMENT=production
```

**Description**: Application environment

**Values**: `development`, `staging`, `production`

**Default**: `production`

**Effects**:
- Logging verbosity
- Debug mode
- Error detail exposure

---

```bash
PORT=8000
```

**Description**: Port for the application to listen on

**Default**: `8000`

**Range**: `1024-65535`

**Note**: Hugging Face Spaces requires port `8000`

---

```bash
WORKERS=4
```

**Description**: Number of uvicorn worker processes

**Default**: `4`

**Recommendations**:
- Development: `1`
- Production: `4-8` (based on CPU cores)
- Formula: `(2 x CPU cores) + 1`

---

#### JWT Configuration (Optional)

```bash
JWT_ALGORITHM=HS256
```

**Description**: JWT signing algorithm

**Default**: `HS256`

**Options**: `HS256`, `HS384`, `HS512`, `RS256`

**Recommendation**: Keep default unless specific requirements

---

```bash
JWT_EXPIRY_DAYS=7
```

**Description**: JWT token expiration in days

**Default**: `7`

**Range**: `1-30`

**Recommendation**: `7` for good balance of security and UX

---

#### SMTP Configuration (Optional)

```bash
SMTP_USE_TLS=true
```

**Description**: Enable TLS/STARTTLS for SMTP

**Default**: `true`

**Values**: `true`, `false`

**Recommendation**: Always use `true` for security

---

```bash
SMTP_TIMEOUT=30
```

**Description**: SMTP connection timeout in seconds

**Default**: `30`

**Range**: `10-60`

---

#### Security & Performance

```bash
RATE_LIMIT_ENABLED=true
```

**Description**: Enable rate limiting for API endpoints

**Default**: `true`

**Values**: `true`, `false`

**Recommendation**: Always `true` in production

---

```bash
RATE_LIMIT_PER_MINUTE=60
```

**Description**: Maximum requests per minute per IP

**Default**: `60`

**Range**: `10-1000`

**Recommendations**:
- Development: `1000` (no limit)
- Production: `60` (1 per second)
- High traffic: `120-300`

---

#### Logging

```bash
LOG_LEVEL=INFO
```

**Description**: Logging verbosity level

**Default**: `INFO`

**Options**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

**Recommendations**:
- Development: `DEBUG`
- Production: `INFO`
- Troubleshooting: `DEBUG`

---

```bash
LOG_FORMAT=json
```

**Description**: Log output format

**Default**: `json`

**Options**: `json`, `text`

**Recommendation**: `json` for production (easier parsing)

---

#### CORS Configuration

```bash
ALLOWED_ORIGINS=http://localhost:3000
```

**Description**: Comma-separated list of allowed CORS origins

**Default**: Value of `FRONTEND_URL`

**Format**: `url1,url2,url3`

**Example**:
```bash
ALLOWED_ORIGINS=https://app.com,https://www.app.com,https://staging.app.com
```

**Note**: Usually not needed if `FRONTEND_URL` is set correctly

---

## Frontend Environment Variables

### Required Variables

```bash
NEXT_PUBLIC_API_URL=https://your-backend.hf.space
```

**Description**: Backend API base URL

**Format**: Full URL with protocol (https://)

**Important**: Must start with `NEXT_PUBLIC_` to be exposed to browser

**Example**:
```bash
NEXT_PUBLIC_API_URL=https://username-todo-backend.hf.space
```

---

### Optional Variables

```bash
BETTER_AUTH_SECRET=<32-character-secret>
```

**Description**: Better Auth secret (if using Better Auth)

**Requirements**: Same as backend JWT secrets

**Note**: Server-side only (no `NEXT_PUBLIC_` prefix)

---

```bash
BETTER_AUTH_URL=https://your-app.vercel.app
```

**Description**: Better Auth callback URL

**Format**: Your Vercel deployment URL

---

## Environment-Specific Configurations

### Development (.env.local)

```bash
# Backend
DATABASE_URL=postgresql+asyncpg://localhost:5432/todo_dev
JWT_SECRET_KEY=dev-secret-key-minimum-32-characters-long
BETTER_AUTH_SECRET=dev-better-auth-secret-32-characters
SMTP_HOST=smtp.mailtrap.io
SMTP_PORT=2525
SMTP_USERNAME=your-mailtrap-username
SMTP_PASSWORD=your-mailtrap-password
SMTP_FROM_EMAIL=dev@localhost
SMTP_FROM_NAME=Todo App Dev
FRONTEND_URL=http://localhost:3000
ENVIRONMENT=development
LOG_LEVEL=DEBUG
RATE_LIMIT_ENABLED=false

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

### Staging

```bash
# Backend
DATABASE_URL=postgresql+asyncpg://staging-db-url
JWT_SECRET_KEY=<staging-secret>
BETTER_AUTH_SECRET=<staging-secret>
SMTP_HOST=smtp.gmail.com
SMTP_USERNAME=staging@yourdomain.com
SMTP_PASSWORD=<app-password>
SMTP_FROM_EMAIL=staging@yourdomain.com
FRONTEND_URL=https://staging.yourdomain.com
ENVIRONMENT=staging
LOG_LEVEL=INFO

# Frontend
NEXT_PUBLIC_API_URL=https://staging-backend.hf.space
```

---

### Production

```bash
# Backend
DATABASE_URL=postgresql+asyncpg://production-db-url
JWT_SECRET_KEY=<production-secret>
BETTER_AUTH_SECRET=<production-secret>
SMTP_HOST=smtp.sendgrid.net
SMTP_USERNAME=apikey
SMTP_PASSWORD=<sendgrid-api-key>
SMTP_FROM_EMAIL=noreply@yourdomain.com
FRONTEND_URL=https://yourdomain.com
ENVIRONMENT=production
LOG_LEVEL=INFO
RATE_LIMIT_ENABLED=true

# Frontend
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

---

## Security Best Practices

### Secret Management

- [ ] Never commit secrets to Git
- [ ] Use different secrets for each environment
- [ ] Rotate secrets regularly (every 90 days)
- [ ] Use strong, random secrets (32+ characters)
- [ ] Store secrets in platform secret managers (Vercel, Hugging Face)

### Access Control

- [ ] Limit who can view/edit secrets
- [ ] Use separate accounts for production
- [ ] Enable 2FA on all accounts
- [ ] Audit secret access regularly

### Validation

- [ ] Validate all required variables on startup
- [ ] Fail fast if variables are missing
- [ ] Log configuration errors clearly
- [ ] Never log secret values

---

## Troubleshooting

### Variable Not Found

**Symptom**: `ValueError: VARIABLE_NAME must be set`

**Causes**:
1. Variable not set in environment
2. Typo in variable name
3. Variable not exported (if using shell)

**Fix**:
```bash
# Check if variable is set
echo $VARIABLE_NAME

# Set variable
export VARIABLE_NAME=value

# Or add to .env file
```

---

### Variable Not Working in Frontend

**Symptom**: `undefined` when accessing variable in browser

**Cause**: Missing `NEXT_PUBLIC_` prefix

**Fix**:
```bash
# ❌ Wrong (not exposed to browser)
API_URL=https://backend.com

# ✅ Correct (exposed to browser)
NEXT_PUBLIC_API_URL=https://backend.com
```

---

### Database Connection Fails

**Symptom**: `ConnectionRefusedError` or `Invalid connection string`

**Checks**:
1. Verify connection string format
2. Ensure `postgresql+asyncpg://` prefix
3. Check host/port are correct
4. Verify credentials
5. Ensure `?sslmode=require` for Neon

---

### SMTP Authentication Fails

**Symptom**: `SMTPAuthenticationError`

**Checks**:
1. Verify username/password are correct
2. Use App Password for Gmail (not main password)
3. Check SMTP host/port
4. Verify TLS settings
5. Ensure account has SMTP enabled

---

## Quick Reference

### Minimum Required Variables

**Backend**:
```bash
DATABASE_URL=postgresql+asyncpg://...
JWT_SECRET_KEY=<32-chars>
BETTER_AUTH_SECRET=<32-chars>
SMTP_HOST=smtp.example.com
SMTP_USERNAME=user
SMTP_PASSWORD=pass
SMTP_FROM_EMAIL=noreply@example.com
FRONTEND_URL=https://app.com
```

**Frontend**:
```bash
NEXT_PUBLIC_API_URL=https://backend.com
```

### Generate Secrets

```bash
# Linux/Mac
openssl rand -base64 32

# Windows PowerShell
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))

# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

### Validate Configuration

```bash
# Check all required variables are set
python scripts/validate_env.py

# Or manually
echo $DATABASE_URL
echo $JWT_SECRET_KEY
echo $SMTP_HOST
```

---

## Related Documentation

- [Hugging Face Deployment](./huggingface.md)
- [Vercel Deployment](./vercel.md)
- [Security Checklist](../production/security.md)
- [Monitoring Guide](../production/monitoring.md)

# Production Security Checklist

**Complete security checklist for production deployment**

---

## Overview

This checklist ensures your Todo application follows security best practices before going live. Review and complete all items before deploying to production.

---

## Pre-Deployment Security

### ✅ Secrets Management

- [ ] **All secrets are stored in environment variables** (not in code)
- [ ] **No secrets committed to Git** (check `.env` files are in `.gitignore`)
- [ ] **JWT_SECRET_KEY is strong** (minimum 32 characters, cryptographically random)
- [ ] **BETTER_AUTH_SECRET is strong** (minimum 32 characters, cryptographically random)
- [ ] **Different secrets for each environment** (dev, staging, production)
- [ ] **Secrets are rotated regularly** (set reminder for 90 days)
- [ ] **SMTP credentials are secure** (using App Password, not main password)
- [ ] **Database credentials are secure** (strong password, limited access)

**Verify**:
```bash
# Check no secrets in Git history
git log --all --full-history --source --pretty=format: -- .env | wc -l
# Should be 0

# Check .gitignore includes .env files
grep -E "^\.env" .gitignore
```

---

### ✅ Database Security

- [ ] **Database uses SSL/TLS** (`?sslmode=require` in connection string)
- [ ] **Database password is strong** (16+ characters, mixed case, numbers, symbols)
- [ ] **Database access is restricted** (IP whitelist or VPC)
- [ ] **Database backups are enabled** (automated daily backups)
- [ ] **Database user has minimum required permissions** (not superuser)
- [ ] **Connection pooling is configured** (prevent connection exhaustion)

**Neon PostgreSQL**:
```bash
# Verify SSL is required
echo $DATABASE_URL | grep "sslmode=require"

# Check connection string format
postgresql+asyncpg://user:pass@host/db?sslmode=require
```

---

### ✅ Authentication & Authorization

- [ ] **JWT tokens expire** (7 days maximum)
- [ ] **Password requirements enforced** (8+ chars, uppercase, lowercase, number, special)
- [ ] **Password reset tokens expire** (1 hour)
- [ ] **Password reset tokens are single-use** (cleared after use)
- [ ] **No email enumeration** (same response for existing/non-existing emails)
- [ ] **Rate limiting enabled** (prevent brute force attacks)
- [ ] **Session management is secure** (tokens stored securely)
- [ ] **User isolation enforced** (users can only access their own data)

**Test**:
```bash
# Test password requirements
curl -X POST https://api.example.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"weak"}'
# Should return 400 with validation error

# Test rate limiting
for i in {1..100}; do
  curl -X POST https://api.example.com/api/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email":"test@example.com","password":"wrong"}'
done
# Should eventually return 429 Too Many Requests
```

---

### ✅ API Security

- [ ] **HTTPS enforced** (all HTTP redirects to HTTPS)
- [ ] **CORS configured correctly** (specific origins, not wildcard `*`)
- [ ] **Security headers present** (see list below)
- [ ] **Input validation on all endpoints** (prevent injection attacks)
- [ ] **SQL injection prevention** (using parameterized queries)
- [ ] **XSS prevention** (proper output encoding)
- [ ] **CSRF protection** (for state-changing operations)
- [ ] **API versioning implemented** (for future compatibility)

**Required Security Headers**:
```http
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
Referrer-Policy: strict-origin-when-cross-origin
```

**Verify Headers**:
```bash
curl -I https://api.example.com/health | grep -E "X-|Strict|Content-Security"
```

---

### ✅ Email Security

- [ ] **SMTP uses TLS** (`SMTP_USE_TLS=true`)
- [ ] **SMTP credentials are secure** (App Password or API key)
- [ ] **Email templates don't expose sensitive data** (no tokens in logs)
- [ ] **Email rate limiting enabled** (prevent spam)
- [ ] **SPF record configured** (for custom domain)
- [ ] **DKIM configured** (for custom domain)
- [ ] **DMARC policy set** (for custom domain)
- [ ] **Unsubscribe link included** (for marketing emails)

**Test Email Security**:
```bash
# Verify TLS is used
openssl s_client -connect smtp.gmail.com:587 -starttls smtp
# Should show TLS connection established
```

---

### ✅ Frontend Security

- [ ] **Environment variables properly scoped** (`NEXT_PUBLIC_` only for client-side)
- [ ] **No secrets in client-side code** (check browser DevTools)
- [ ] **Content Security Policy configured** (prevent XSS)
- [ ] **Subresource Integrity for CDN resources** (if using CDN)
- [ ] **Secure cookies** (HttpOnly, Secure, SameSite flags)
- [ ] **Input sanitization** (prevent XSS in user input)
- [ ] **Output encoding** (escape HTML in user-generated content)

**Verify**:
```bash
# Check no secrets exposed in browser
# Open DevTools → Sources → Search for "secret", "password", "key"

# Check CSP header
curl -I https://app.example.com | grep "Content-Security-Policy"
```

---

## Deployment Security

### ✅ Platform Configuration

**Hugging Face Spaces**:
- [ ] **Space visibility set correctly** (Private for sensitive apps)
- [ ] **Secrets configured in Space settings** (not in Dockerfile)
- [ ] **Docker image from trusted base** (official python:3.13-slim)
- [ ] **No unnecessary packages installed** (minimal attack surface)
- [ ] **Health check endpoint enabled** (for monitoring)

**Vercel**:
- [ ] **Environment variables scoped correctly** (Production, Preview, Development)
- [ ] **Deployment protection enabled** (password or Vercel Auth)
- [ ] **Custom domain uses HTTPS** (automatic with Vercel)
- [ ] **Preview deployments protected** (not publicly accessible)

---

### ✅ Network Security

- [ ] **All traffic uses HTTPS** (no HTTP endpoints)
- [ ] **TLS 1.2 or higher** (no outdated protocols)
- [ ] **Strong cipher suites** (no weak ciphers)
- [ ] **HSTS enabled** (force HTTPS)
- [ ] **Certificate is valid** (not expired, correct domain)
- [ ] **No mixed content** (all resources loaded via HTTPS)

**Test**:
```bash
# Check TLS version
openssl s_client -connect api.example.com:443 -tls1_2

# Check certificate
openssl s_client -connect api.example.com:443 -showcerts

# Test SSL configuration
# Use: https://www.ssllabs.com/ssltest/
```

---

### ✅ Logging & Monitoring

- [ ] **Sensitive data not logged** (no passwords, tokens, emails in logs)
- [ ] **Log levels appropriate** (INFO in production, not DEBUG)
- [ ] **Logs are structured** (JSON format for parsing)
- [ ] **Log retention policy set** (30-90 days)
- [ ] **Error tracking configured** (Sentry, Rollbar, etc.)
- [ ] **Uptime monitoring enabled** (health check pings)
- [ ] **Alert thresholds configured** (notify on errors)

**Verify Logs Don't Expose Secrets**:
```bash
# Check logs for sensitive patterns
grep -iE "(password|secret|token|key)" logs/*.log
# Should find no matches
```

---

## Post-Deployment Security

### ✅ Monitoring & Alerts

- [ ] **Health check monitoring** (ping every 5 minutes)
- [ ] **Error rate monitoring** (alert on >1% error rate)
- [ ] **Response time monitoring** (alert on >2s p95)
- [ ] **Database connection monitoring** (alert on connection failures)
- [ ] **SMTP delivery monitoring** (alert on email failures)
- [ ] **Disk space monitoring** (alert at 80% capacity)
- [ ] **Memory usage monitoring** (alert at 90% usage)

**Setup Monitoring**:
```bash
# Use services like:
# - UptimeRobot (free health check monitoring)
# - Better Uptime (advanced monitoring)
# - Sentry (error tracking)
# - Datadog (comprehensive monitoring)
```

---

### ✅ Incident Response

- [ ] **Incident response plan documented** (who to contact, steps to take)
- [ ] **Rollback procedure tested** (can revert to previous version)
- [ ] **Backup restoration tested** (can restore from backup)
- [ ] **Security contact published** (security@yourdomain.com)
- [ ] **Vulnerability disclosure policy** (how to report issues)
- [ ] **On-call rotation defined** (who responds to alerts)

---

### ✅ Regular Maintenance

- [ ] **Dependencies updated monthly** (security patches)
- [ ] **Security audit quarterly** (review this checklist)
- [ ] **Penetration testing annually** (professional security assessment)
- [ ] **Secrets rotated every 90 days** (JWT keys, SMTP passwords)
- [ ] **Access review quarterly** (remove unused accounts)
- [ ] **Backup restoration tested quarterly** (verify backups work)

**Update Dependencies**:
```bash
# Backend
cd backend
pip list --outdated
pip install --upgrade <package>

# Frontend
cd frontend
npm outdated
npm update
```

---

## Compliance & Legal

### ✅ Data Protection

- [ ] **Privacy policy published** (GDPR, CCPA compliance)
- [ ] **Terms of service published** (user agreement)
- [ ] **Cookie consent implemented** (if using cookies)
- [ ] **Data retention policy defined** (how long data is kept)
- [ ] **Data deletion process** (user can request deletion)
- [ ] **Data export process** (user can download their data)
- [ ] **Data breach notification plan** (72-hour notification)

---

### ✅ User Privacy

- [ ] **Minimal data collection** (only collect what's needed)
- [ ] **User consent obtained** (for data processing)
- [ ] **Data encrypted at rest** (database encryption)
- [ ] **Data encrypted in transit** (HTTPS, TLS)
- [ ] **PII handling documented** (how personal data is used)
- [ ] **Third-party data sharing disclosed** (if any)
- [ ] **User rights respected** (access, rectification, erasure)

---

## Security Testing

### ✅ Automated Testing

- [ ] **Unit tests for authentication** (password validation, JWT generation)
- [ ] **Integration tests for API** (all endpoints tested)
- [ ] **Security tests for injection** (SQL injection, XSS)
- [ ] **Rate limiting tests** (verify limits work)
- [ ] **CORS tests** (verify only allowed origins)
- [ ] **CI/CD security scanning** (dependency vulnerabilities)

**Run Security Tests**:
```bash
# Backend tests
cd backend
pytest tests/ -v

# Security scanning
pip install safety
safety check

# Dependency audit
pip-audit
```

---

### ✅ Manual Testing

- [ ] **Password reset flow tested** (end-to-end)
- [ ] **Email delivery tested** (receive emails)
- [ ] **CORS tested** (from frontend domain)
- [ ] **Rate limiting tested** (trigger limits)
- [ ] **Error handling tested** (graceful failures)
- [ ] **Session management tested** (logout, token expiry)

---

## Security Incident Checklist

If a security incident occurs:

### Immediate Actions (0-1 hour)

1. [ ] **Assess severity** (data breach, service disruption, etc.)
2. [ ] **Contain the incident** (disable affected systems if needed)
3. [ ] **Notify team** (security team, management)
4. [ ] **Preserve evidence** (logs, screenshots)
5. [ ] **Document timeline** (what happened when)

### Short-term Actions (1-24 hours)

1. [ ] **Investigate root cause** (how did it happen)
2. [ ] **Implement fix** (patch vulnerability)
3. [ ] **Rotate compromised secrets** (all affected credentials)
4. [ ] **Notify affected users** (if data breach)
5. [ ] **Update security measures** (prevent recurrence)

### Long-term Actions (1-7 days)

1. [ ] **Post-mortem analysis** (what went wrong, lessons learned)
2. [ ] **Update security policies** (based on learnings)
3. [ ] **Improve monitoring** (detect similar issues earlier)
4. [ ] **Train team** (prevent future incidents)
5. [ ] **Report to authorities** (if required by law)

---

## Security Resources

### Tools

- **SSL Testing**: https://www.ssllabs.com/ssltest/
- **Security Headers**: https://securityheaders.com/
- **OWASP ZAP**: https://www.zaproxy.org/ (penetration testing)
- **Snyk**: https://snyk.io/ (dependency scanning)
- **Safety**: https://pyup.io/safety/ (Python security)

### References

- **OWASP Top 10**: https://owasp.org/www-project-top-ten/
- **OWASP API Security**: https://owasp.org/www-project-api-security/
- **CWE Top 25**: https://cwe.mitre.org/top25/
- **NIST Cybersecurity Framework**: https://www.nist.gov/cyberframework

---

## Sign-off

Before deploying to production, have the following people review and sign off:

- [ ] **Developer**: Code reviewed, tests pass
- [ ] **Security Lead**: Security checklist complete
- [ ] **DevOps**: Infrastructure configured correctly
- [ ] **Product Owner**: Features work as expected
- [ ] **Legal**: Compliance requirements met

**Deployment Date**: _______________

**Approved By**: _______________

---

## Quick Reference

### Critical Security Items

**Must Have**:
1. ✅ All secrets in environment variables (not code)
2. ✅ HTTPS enforced everywhere
3. ✅ Database uses SSL
4. ✅ Strong passwords required
5. ✅ Rate limiting enabled
6. ✅ CORS configured (not wildcard)
7. ✅ Security headers present
8. ✅ Logs don't expose secrets

**Test Commands**:
```bash
# Check secrets not in Git
git log --all --full-history -- .env

# Check HTTPS
curl -I https://api.example.com

# Check security headers
curl -I https://api.example.com | grep -E "X-|Strict|Content-Security"

# Check rate limiting
for i in {1..100}; do curl https://api.example.com/api/auth/login; done
```

---

## Related Documentation

- [Environment Variables](../deployment/environment.md)
- [Hugging Face Deployment](../deployment/huggingface.md)
- [Vercel Deployment](../deployment/vercel.md)
- [Monitoring Guide](./monitoring.md)

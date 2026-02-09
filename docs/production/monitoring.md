# Production Monitoring Guide

**Comprehensive guide for monitoring your Todo application in production**

---

## Overview

This guide covers monitoring, logging, alerting, and observability for your production deployment. Proper monitoring helps you detect issues early, understand user behavior, and maintain high availability.

---

## Monitoring Strategy

### The Four Golden Signals

Monitor these key metrics for any production system:

1. **Latency**: How long requests take to complete
2. **Traffic**: How many requests you're receiving
3. **Errors**: Rate of failed requests
4. **Saturation**: How "full" your service is (CPU, memory, disk)

---

## Health Check Monitoring

### Endpoint

```http
GET /health
```

**Response (Healthy)**:
```json
{
  "status": "healthy",
  "timestamp": "2026-02-08T12:00:00Z",
  "version": "0.1.0",
  "database": "connected",
  "smtp": "configured"
}
```

**Response (Unhealthy)**:
```json
{
  "status": "unhealthy",
  "timestamp": "2026-02-08T12:00:00Z",
  "version": "0.1.0",
  "database": "error",
  "smtp": "configured",
  "errors": [
    "Database: Connection refused"
  ]
}
```

### Setup Monitoring

#### Option 1: UptimeRobot (Free)

1. Sign up at [uptimerobot.com](https://uptimerobot.com)
2. Create new monitor:
   - **Monitor Type**: HTTP(s)
   - **Friendly Name**: Todo Backend Health
   - **URL**: `https://your-backend.hf.space/health`
   - **Monitoring Interval**: 5 minutes
   - **Monitor Timeout**: 30 seconds
3. Add alert contacts (email, SMS, Slack)
4. Save monitor

**Expected**: 99.9%+ uptime

#### Option 2: Better Uptime (Advanced)

1. Sign up at [betteruptime.com](https://betteruptime.com)
2. Create monitor with:
   - **URL**: `https://your-backend.hf.space/health`
   - **Check frequency**: 30 seconds
   - **Expected status**: 200
   - **Expected response**: Contains `"status":"healthy"`
3. Configure on-call schedule
4. Set up incident management

#### Option 3: Custom Script

```bash
#!/bin/bash
# health-check.sh

BACKEND_URL="https://your-backend.hf.space"
WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

response=$(curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL/health")

if [ "$response" != "200" ]; then
  curl -X POST "$WEBHOOK_URL" \
    -H 'Content-Type: application/json' \
    -d "{\"text\":\"🚨 Backend health check failed! Status: $response\"}"
fi
```

**Run with cron**:
```bash
# Check every 5 minutes
*/5 * * * * /path/to/health-check.sh
```

---

## Application Metrics

### Key Metrics to Track

#### API Performance

```
# Request rate
requests_per_second
requests_per_minute

# Response time
response_time_p50  # Median
response_time_p95  # 95th percentile
response_time_p99  # 99th percentile
response_time_max  # Maximum

# Error rate
error_rate_percent
errors_per_minute
```

**Targets**:
- P95 latency: < 500ms
- P99 latency: < 1000ms
- Error rate: < 1%
- Availability: > 99.9%

#### Database Metrics

```
# Connection pool
db_connections_active
db_connections_idle
db_connections_max

# Query performance
db_query_time_avg
db_query_time_max
db_slow_queries_count

# Database size
db_size_mb
db_table_sizes
```

**Alerts**:
- Connection pool > 80% → Scale up
- Slow queries > 1s → Optimize
- Database size > 80% → Cleanup or upgrade

#### Email Metrics

```
# Delivery
emails_sent_total
emails_failed_total
email_delivery_rate_percent

# Performance
email_send_time_avg
email_queue_length
```

**Alerts**:
- Delivery rate < 95% → Check SMTP
- Queue length > 100 → Investigate backlog

---

## Logging

### Log Levels

Use appropriate log levels:

```python
# DEBUG: Detailed diagnostic information
logger.debug("User query: SELECT * FROM users WHERE id=%s", user_id)

# INFO: General informational messages
logger.info("User logged in successfully: user_id=%s", user_id)

# WARNING: Warning messages for potentially harmful situations
logger.warning("Rate limit approaching for IP: %s", ip_address)

# ERROR: Error messages for failures
logger.error("Failed to send email: %s", error)

# CRITICAL: Critical errors requiring immediate attention
logger.critical("Database connection lost")
```

**Production**: Use `INFO` level (not `DEBUG`)

### Structured Logging

Use JSON format for easy parsing:

```json
{
  "timestamp": "2026-02-08T12:00:00Z",
  "level": "INFO",
  "message": "User logged in",
  "user_id": "123",
  "ip_address": "192.168.1.1",
  "request_id": "abc-123",
  "duration_ms": 45
}
```

**Benefits**:
- Easy to search and filter
- Machine-readable
- Structured data extraction

### Log Aggregation

#### Option 1: Hugging Face Spaces Logs

View logs directly in Hugging Face:
1. Go to your Space
2. Click "Logs" tab
3. View real-time logs

**Limitations**:
- No long-term retention
- Limited search capabilities
- No alerting

#### Option 2: External Log Service

**Logtail** (Recommended):
```python
# Install
pip install logtail-python

# Configure
import logging
from logtail import LogtailHandler

handler = LogtailHandler(source_token="YOUR_TOKEN")
logger = logging.getLogger(__name__)
logger.addHandler(handler)
```

**Papertrail**:
```bash
# Forward logs via syslog
# Add to Dockerfile:
RUN apt-get install -y rsyslog
# Configure rsyslog to forward to Papertrail
```

**Datadog**:
```python
# Install
pip install ddtrace

# Run with Datadog agent
DD_SERVICE=todo-backend \
DD_ENV=production \
DD_VERSION=0.1.0 \
ddtrace-run uvicorn main:app
```

### What to Log

**✅ DO Log**:
- User actions (login, logout, create, update, delete)
- API requests (method, path, status, duration)
- Errors and exceptions (with stack traces)
- Performance metrics (slow queries, high latency)
- Security events (failed logins, rate limits)

**❌ DON'T Log**:
- Passwords or password hashes
- JWT tokens or session IDs
- Email addresses (sanitize: `u***@example.com`)
- Credit card numbers
- API keys or secrets

### Log Retention

**Recommendations**:
- **Production**: 30-90 days
- **Staging**: 7-30 days
- **Development**: 1-7 days

**Compliance**: Check legal requirements (GDPR, HIPAA, etc.)

---

## Error Tracking

### Sentry Integration

**Setup**:
```python
# Install
pip install sentry-sdk[fastapi]

# Configure in main.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="YOUR_SENTRY_DSN",
    environment="production",
    traces_sample_rate=0.1,  # 10% of transactions
    integrations=[FastApiIntegration()],
)
```

**Benefits**:
- Automatic error capture
- Stack traces with context
- Release tracking
- Performance monitoring
- User feedback

**Alerts**:
- New error types
- Error rate spikes
- Performance degradation

### Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": {
      "field": "email",
      "value": "invalid-email"
    },
    "request_id": "abc-123",
    "timestamp": "2026-02-08T12:00:00Z"
  }
}
```

---

## Performance Monitoring

### Application Performance Monitoring (APM)

#### Datadog APM

```python
# Install
pip install ddtrace

# Run with tracing
DD_SERVICE=todo-backend \
DD_ENV=production \
DD_TRACE_ENABLED=true \
ddtrace-run uvicorn main:app
```

**Metrics**:
- Request latency by endpoint
- Database query performance
- External API calls
- Error rates by endpoint

#### New Relic

```python
# Install
pip install newrelic

# Configure
newrelic-admin generate-config YOUR_LICENSE_KEY newrelic.ini

# Run
NEW_RELIC_CONFIG_FILE=newrelic.ini \
newrelic-admin run-program uvicorn main:app
```

### Database Query Monitoring

**Slow Query Log**:
```python
# Log queries > 1 second
import time
from functools import wraps

def log_slow_queries(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        duration = time.time() - start

        if duration > 1.0:
            logger.warning(
                "Slow query detected",
                extra={
                    "function": func.__name__,
                    "duration_seconds": duration
                }
            )
        return result
    return wrapper
```

**Query Optimization**:
- Add indexes for frequently queried fields
- Use connection pooling
- Implement caching for repeated queries
- Monitor N+1 query problems

---

## Alerting

### Alert Channels

**Email**:
- Good for: Non-urgent alerts
- Response time: Hours

**SMS**:
- Good for: Urgent alerts
- Response time: Minutes

**Slack/Discord**:
- Good for: Team notifications
- Response time: Minutes to hours

**PagerDuty**:
- Good for: Critical incidents
- Response time: Immediate

### Alert Rules

#### Critical Alerts (Immediate Response)

```yaml
# Service Down
- name: Backend Down
  condition: health_check_status != 200
  duration: 2 minutes
  severity: critical
  channels: [pagerduty, sms]

# Database Connection Lost
- name: Database Unreachable
  condition: db_connection_errors > 0
  duration: 1 minute
  severity: critical
  channels: [pagerduty, sms]

# High Error Rate
- name: Error Rate Spike
  condition: error_rate > 5%
  duration: 5 minutes
  severity: critical
  channels: [pagerduty, slack]
```

#### Warning Alerts (Review Soon)

```yaml
# Slow Response Time
- name: High Latency
  condition: response_time_p95 > 1000ms
  duration: 10 minutes
  severity: warning
  channels: [slack, email]

# High Memory Usage
- name: Memory Usage High
  condition: memory_usage > 80%
  duration: 15 minutes
  severity: warning
  channels: [slack]

# Email Delivery Issues
- name: Email Failures
  condition: email_failure_rate > 10%
  duration: 30 minutes
  severity: warning
  channels: [slack, email]
```

#### Info Alerts (FYI)

```yaml
# Deployment
- name: New Deployment
  condition: deployment_event
  severity: info
  channels: [slack]

# High Traffic
- name: Traffic Spike
  condition: requests_per_minute > 1000
  duration: 5 minutes
  severity: info
  channels: [slack]
```

### Alert Fatigue Prevention

**Best Practices**:
- Set appropriate thresholds (not too sensitive)
- Use duration windows (avoid flapping)
- Group related alerts
- Implement alert suppression during maintenance
- Review and tune alerts regularly

---

## Dashboards

### Essential Dashboards

#### 1. Overview Dashboard

**Metrics**:
- Request rate (requests/minute)
- Error rate (%)
- Response time (P50, P95, P99)
- Active users
- Database connections
- Memory/CPU usage

**Time range**: Last 24 hours

#### 2. API Performance Dashboard

**Metrics per endpoint**:
- Request count
- Average response time
- Error rate
- Slowest requests

**Grouping**: By endpoint, method, status code

#### 3. Database Dashboard

**Metrics**:
- Query performance
- Connection pool usage
- Slow queries
- Database size
- Table sizes

#### 4. User Activity Dashboard

**Metrics**:
- Active users (hourly, daily)
- New registrations
- Login attempts (success/failure)
- Password resets requested
- Todos created/completed

### Dashboard Tools

**Grafana** (Self-hosted):
- Flexible and powerful
- Supports multiple data sources
- Free and open source

**Datadog** (SaaS):
- All-in-one solution
- Easy setup
- Paid service

**Hugging Face Spaces** (Built-in):
- Basic metrics available
- Limited customization

---

## Synthetic Monitoring

### What is Synthetic Monitoring?

Automated tests that simulate user behavior to detect issues before real users encounter them.

### Setup Synthetic Tests

```python
# synthetic_tests.py
import requests
import time

def test_user_registration():
    """Test user registration flow"""
    start = time.time()

    response = requests.post(
        "https://api.example.com/api/auth/register",
        json={
            "email": f"test+{int(time.time())}@example.com",
            "password": "TestPass123!"
        }
    )

    duration = time.time() - start

    assert response.status_code == 201
    assert duration < 2.0  # Should complete in < 2s

    return {
        "test": "user_registration",
        "status": "pass",
        "duration": duration
    }

def test_health_check():
    """Test health check endpoint"""
    response = requests.get("https://api.example.com/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"

    return {"test": "health_check", "status": "pass"}

# Run every 5 minutes
if __name__ == "__main__":
    tests = [test_health_check, test_user_registration]

    for test in tests:
        try:
            result = test()
            print(f"✅ {result['test']}: PASS")
        except Exception as e:
            print(f"❌ {result['test']}: FAIL - {e}")
            # Send alert
```

**Run with cron**:
```bash
*/5 * * * * python /path/to/synthetic_tests.py
```

---

## Incident Response

### Incident Severity Levels

**SEV1 - Critical**:
- Service completely down
- Data breach or security incident
- Response time: Immediate
- Example: Database connection lost

**SEV2 - High**:
- Major feature broken
- High error rate (>5%)
- Response time: < 1 hour
- Example: Email service down

**SEV3 - Medium**:
- Minor feature broken
- Performance degradation
- Response time: < 4 hours
- Example: Slow API responses

**SEV4 - Low**:
- Cosmetic issues
- Non-critical bugs
- Response time: Next business day
- Example: Typo in email template

### Incident Response Process

1. **Detect**: Alert fires or user reports issue
2. **Acknowledge**: Team member acknowledges alert
3. **Assess**: Determine severity and impact
4. **Communicate**: Notify stakeholders
5. **Investigate**: Find root cause
6. **Mitigate**: Implement temporary fix
7. **Resolve**: Deploy permanent fix
8. **Post-mortem**: Document learnings

### Status Page

**Setup**:
1. Use service like [status.io](https://status.io) or [statuspage.io](https://statuspage.io)
2. Configure components:
   - API
   - Database
   - Email Service
3. Integrate with monitoring
4. Publish status page URL

**Example**: `https://status.todoapp.com`

---

## Monitoring Checklist

### Initial Setup

- [ ] Health check monitoring configured (UptimeRobot/Better Uptime)
- [ ] Error tracking configured (Sentry)
- [ ] Log aggregation configured (Logtail/Papertrail)
- [ ] APM configured (Datadog/New Relic) - optional
- [ ] Alert channels configured (Email, Slack, SMS)
- [ ] Dashboards created (Overview, API, Database)
- [ ] Synthetic tests running (every 5 minutes)
- [ ] Status page published (optional)

### Daily Checks

- [ ] Review error logs for new issues
- [ ] Check response time trends
- [ ] Monitor error rate
- [ ] Review slow queries
- [ ] Check disk space usage

### Weekly Reviews

- [ ] Review alert history
- [ ] Analyze performance trends
- [ ] Check for security incidents
- [ ] Review user activity patterns
- [ ] Update dashboards if needed

### Monthly Tasks

- [ ] Review and tune alert thresholds
- [ ] Analyze cost vs. usage
- [ ] Update monitoring documentation
- [ ] Test incident response procedures
- [ ] Review log retention policies

---

## Cost Optimization

### Free Tier Options

**Monitoring**:
- UptimeRobot: 50 monitors free
- Better Uptime: 10 monitors free
- Sentry: 5,000 errors/month free

**Logging**:
- Logtail: 1GB/month free
- Papertrail: 50MB/day free

**APM**:
- Datadog: 14-day trial
- New Relic: 100GB/month free

### Paid Recommendations

**Small Scale** (<10k requests/day):
- UptimeRobot Pro: $7/month
- Sentry Team: $26/month
- Logtail: $10/month
- **Total**: ~$43/month

**Medium Scale** (<100k requests/day):
- Better Uptime: $20/month
- Sentry Business: $80/month
- Datadog: $15/host/month
- **Total**: ~$115/month

---

## Quick Reference

### Essential Monitoring URLs

```
Health Check: https://your-backend.hf.space/health
API Docs: https://your-backend.hf.space/docs
Logs: https://huggingface.co/spaces/YOUR_USERNAME/todo-backend/logs
```

### Key Metrics Targets

```
Availability: > 99.9%
P95 Latency: < 500ms
Error Rate: < 1%
Database Connections: < 80% of max
Memory Usage: < 80%
```

### Alert Response Times

```
Critical (SEV1): Immediate
High (SEV2): < 1 hour
Medium (SEV3): < 4 hours
Low (SEV4): Next business day
```

---

## Related Documentation

- [Security Checklist](./security.md)
- [Hugging Face Deployment](../deployment/huggingface.md)
- [Vercel Deployment](../deployment/vercel.md)
- [Environment Variables](../deployment/environment.md)

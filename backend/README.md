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

FastAPI backend for Todo application with JWT authentication, email notifications, and PostgreSQL database.

## Features

- 🚀 **FastAPI Framework**: High-performance async API
- 🔐 **JWT Authentication**: Secure token-based auth with Better Auth integration
- 📧 **Email Service**: Password reset via SMTP (async with aiosmtplib)
- 🗄️ **PostgreSQL Database**: Neon Serverless PostgreSQL with SQLModel ORM
- 🐳 **Docker Containerized**: Multi-stage build for production deployment
- ✅ **Health Check**: Built-in monitoring endpoint
- 🔒 **Security**: Rate limiting, CORS, security headers
- 📊 **API Documentation**: Auto-generated Swagger UI and ReDoc

## API Documentation

Once deployed, visit:
- **Swagger UI**: `https://your-space-url/docs`
- **ReDoc**: `https://your-space-url/redoc`
- **Health Check**: `https://your-space-url/health`

## Environment Variables

See [Environment Variables Reference](../docs/deployment/environment.md) for complete documentation.

## Deployment

See [Hugging Face Deployment Guide](../docs/deployment/huggingface.md) for detailed instructions.

---

**Built with ❤️ using FastAPI and deployed on Hugging Face Spaces**

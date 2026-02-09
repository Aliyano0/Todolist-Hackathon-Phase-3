# Database Driver: psycopg2-binary for Python 3.13 Compatibility

## Final Solution

After extensive testing with multiple PostgreSQL drivers, **psycopg2-binary==2.9.10** emerged as the optimal choice for this project.

## Migration Journey

### Attempted Solutions
1. **psycopg2-binary==2.9.9** (original) - Installation issues in some environments
2. **asyncpg==0.29.0** - Python 3.13 compilation errors
3. **asyncpg==0.30.0** - MissingGreenlet error (async/sync incompatibility with SQLModel)
4. **psycopg[binary]==3.2.1** - No Python 3.13 wheels available

### Final Solution: psycopg2-binary==2.9.10

**Why psycopg2-binary==2.9.10?**
- ✅ Full Python 3.13 support
- ✅ Perfect synchronous SQLModel compatibility
- ✅ Excellent Neon Serverless PostgreSQL support
- ✅ Stable, mature, widely-used driver
- ✅ Standard PostgreSQL connection parameters
- ✅ No async/sync complexity

## Requirements

```txt
psycopg2-binary==2.9.10
```

## Database Configuration

```python
from sqlmodel import create_engine
from sqlalchemy.pool import QueuePool
import os

DATABASE_URL = os.getenv("NEON_DATABASE_URL", "postgresql://...")

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    echo=False
)
```

## Key Learnings from Migration Journey

### 1. Python 3.13 Compatibility Issues
- **asyncpg 0.29.0**: C extension compilation failures due to Python 3.13 C API changes
- **asyncpg 0.30.0**: Fixed C API issues but introduced async/sync incompatibility
- **psycopg 3.2.1**: No Python 3.13 wheels available (only supports Python 3.8-3.12)
- **psycopg2-binary 2.9.10**: Full Python 3.13 support ✅

### 2. Async/Sync Architecture Mismatch
**asyncpg** is fundamentally incompatible with synchronous SQLModel:
- asyncpg requires async/await operations exclusively
- SQLModel uses synchronous database operations
- Mixing them requires greenlet support: `MissingGreenlet: greenlet_spawn has not been called`
- No simple configuration fix - architectural incompatibility

### 3. Driver Maturity and Ecosystem Support
- **psycopg2**: Mature, stable, 15+ years of production use
- **psycopg3**: Modern rewrite but limited Python 3.13 support (as of 2026-02)
- **asyncpg**: Excellent for async-native applications, not for sync ORMs

## Database Schema Fix Required

The existing database has a type mismatch that must be fixed before the server can start:

**Problem**: `user` table has `id` column as VARCHAR, but User model defines it as UUID

**Solution**: Run the schema fix migration:

```bash
cd backend
python database/fix_user_schema.py
```

This will drop and recreate the `user` and `authentication_token` tables with correct UUID types.

## Final Configuration

### Requirements
```txt
psycopg2-binary==2.9.10
```

### Database Session
```python
from sqlmodel import create_engine
from sqlalchemy.pool import QueuePool
import os

DATABASE_URL = os.getenv("NEON_DATABASE_URL", "postgresql://...")

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    echo=False
)
```

## Compatibility
- ✅ Full Python 3.13 support
- ✅ Synchronous SQLModel operations
- ✅ Neon Serverless PostgreSQL with SSL
- ✅ Standard PostgreSQL connection parameters
- ✅ Mature, production-ready driver
- ✅ No async/sync complexity
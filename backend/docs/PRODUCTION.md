# Production Documentation

## PROD-01: Health Check Endpoints

- `/health` - General health check
- `/healthz` - Liveness probe
- `/readyz` - Readiness probe with DB check

## PROD-02: Structured Logging

- JSON format in production
- Human-readable in development
- Log levels: DEBUG, INFO, WARNING, ERROR
- Request ID tracing

## PROD-03: Error Tracking

- Structured error logging
- Exception context capture
- Error level classification

## PROD-04: Backup Procedures

### Database Backup
```bash
# SQLite backup
cp data/cc_video.db data/cc_video.db.backup

# Or use sqlite3
sqlite3 data/cc_video.db ".backup data/cc_video.db.backup"
```

### Restore
```bash
# Restore from backup
cp data/cc_video.db.backup data/cc_video.db
```

## PROD-05: Deployment

### Docker Compose
```bash
# Build and start
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop
docker-compose -f docker-compose.prod.yml down
```

### Environment Variables
- `SECRET_KEY` - JWT secret key
- `DATABASE_URL` - Database connection string
- `DEBUG` - Enable debug mode (true/false)
- `CORS_ORIGINS` - Allowed CORS origins

---

*Production docs updated: 2026-04-30*

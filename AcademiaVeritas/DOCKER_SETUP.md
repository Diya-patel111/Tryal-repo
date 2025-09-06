# AcademiaVeritas Docker Setup

This document provides comprehensive instructions for containerizing and running the AcademiaVeritas application using Docker and Docker Compose.

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed and running
- Docker Compose v3.8+
- Git (for cloning the repository)

### One-Command Setup
```bash
# Clone the repository
git clone <repository-url>
cd AcademiaVeritas

# Start the application
./scripts/start.sh start
```

The application will be available at:
- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:5001
- **Database**: localhost:5432

## 📁 Project Structure

```
AcademiaVeritas/
├── Dockerfile.backend          # Backend container configuration
├── Dockerfile.frontend         # Frontend container configuration
├── docker-compose.yml          # Production orchestration
├── docker-compose.dev.yml      # Development orchestration
├── .dockerignore              # Docker ignore patterns
├── scripts/
│   └── start.sh               # Management script
├── frontend/
│   └── nginx.conf             # Nginx configuration
└── backend/
    ├── .env                   # Environment variables
    └── requirements.txt       # Python dependencies
```

## 🐳 Container Architecture

### Services Overview

| Service | Container | Port | Description |
|---------|-----------|------|-------------|
| **Frontend** | academia_frontend | 8080 | React app served by Nginx |
| **Backend** | academia_backend | 5001 | Python Flask API with Gunicorn |
| **Database** | academia_db | 5432 | PostgreSQL 14 database |
| **Redis** | academia_redis | 6379 | Redis cache (optional) |

### Network Architecture
- All services communicate through a custom bridge network
- Frontend proxies API requests to backend
- Backend connects to database and Redis
- Health checks ensure service availability

## 🛠️ Configuration Files

### 1. Dockerfile.backend
- **Base Image**: Python 3.10-slim
- **WSGI Server**: Gunicorn with 4 workers
- **Dependencies**: All Python packages + system libraries
- **Security**: Non-root user execution
- **Optimization**: Multi-layer caching

### 2. Dockerfile.frontend
- **Multi-stage Build**: Node.js build + Nginx serve
- **Base Image**: nginx:stable-alpine
- **Features**: Gzip compression, security headers
- **SPA Support**: Client-side routing support
- **Health Checks**: Built-in health monitoring

### 3. docker-compose.yml
- **Production Ready**: Optimized for production deployment
- **Health Checks**: All services have health monitoring
- **Volume Persistence**: Data persistence across restarts
- **Environment Variables**: Secure configuration management

## 🔧 Environment Configuration

### Required Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Database
DATABASE_URL=postgresql://admin:admin@db:5432/academia_veritas

# Security
SECRET_KEY=your-secret-key-change-in-production

# Blockchain (Optional)
INFURA_API_KEY=your-infura-api-key
CONTRACT_ADDRESS=your-contract-address
WALLET_PRIVATE_KEY=your-wallet-private-key
WALLET_ADDRESS=your-wallet-address
```

### Environment Files
- **Production**: Uses `docker-compose.yml`
- **Development**: Uses `docker-compose.dev.yml`
- **Local Override**: Create `.env.local` for local overrides

## 🚀 Management Commands

### Using the Management Script

```bash
# Start production environment
./scripts/start.sh start

# Start development environment
./scripts/start.sh dev

# Stop production environment
./scripts/start.sh stop

# Stop development environment
./scripts/start.sh stop-dev

# View logs
./scripts/start.sh logs
./scripts/start.sh logs dev

# Check status
./scripts/start.sh status

# Clean up everything
./scripts/start.sh cleanup

# Show help
./scripts/start.sh help
```

### Using Docker Compose Directly

```bash
# Production
docker-compose up --build -d
docker-compose down

# Development
docker-compose -f docker-compose.dev.yml up --build -d
docker-compose -f docker-compose.dev.yml down

# View logs
docker-compose logs -f
docker-compose -f docker-compose.dev.yml logs -f

# Scale services
docker-compose up --scale backend=3
```

## 🔍 Monitoring and Debugging

### Health Checks
All services include health checks:
- **Database**: PostgreSQL connection test
- **Backend**: HTTP health endpoint
- **Frontend**: Nginx health check
- **Redis**: Redis ping test

### Viewing Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db

# Development logs
docker-compose -f docker-compose.dev.yml logs -f
```

### Container Status
```bash
# Check running containers
docker-compose ps

# Check resource usage
docker stats

# Inspect specific container
docker inspect academia_backend
```

## 🛡️ Security Features

### Container Security
- **Non-root Users**: All containers run as non-root
- **Minimal Base Images**: Alpine Linux for smaller attack surface
- **Security Headers**: Nginx configured with security headers
- **Network Isolation**: Custom network with restricted access

### Data Security
- **Volume Encryption**: Docker volumes for data persistence
- **Environment Variables**: Sensitive data in environment files
- **Database Security**: PostgreSQL with authentication
- **API Security**: CORS and authentication middleware

## 📊 Performance Optimization

### Backend Optimizations
- **Gunicorn Workers**: 4 worker processes for concurrency
- **Connection Pooling**: Database connection optimization
- **Caching**: Redis for session and data caching
- **Static Files**: Nginx serves static assets efficiently

### Frontend Optimizations
- **Gzip Compression**: Reduces bandwidth usage
- **Asset Caching**: Long-term caching for static assets
- **CDN Ready**: Optimized for CDN deployment
- **Bundle Splitting**: Efficient JavaScript bundling

### Database Optimizations
- **Connection Limits**: Optimized PostgreSQL settings
- **Indexing**: Proper database indexing
- **Query Optimization**: Efficient database queries
- **Backup Strategy**: Automated backup procedures

## 🔄 Development Workflow

### Development Environment
```bash
# Start development environment
./scripts/start.sh dev

# The development environment includes:
# - Hot reloading for backend changes
# - Volume mounting for live code updates
# - Debug logging enabled
# - Separate database for development
```

### Code Changes
- **Backend**: Changes are reflected immediately (volume mounted)
- **Frontend**: Requires rebuild for production changes
- **Database**: Schema changes require migration

### Testing
```bash
# Run tests in container
docker-compose exec backend python -m pytest

# Run specific test
docker-compose exec backend python -m pytest tests/test_auth.py

# Run frontend tests
docker-compose exec frontend npm test
```

## 🚀 Deployment

### Production Deployment
1. **Environment Setup**: Configure production environment variables
2. **Build Images**: Build optimized production images
3. **Deploy**: Use `docker-compose up -d` for production
4. **Monitor**: Set up monitoring and logging

### Cloud Deployment
- **AWS ECS**: Use ECS task definitions
- **Google Cloud Run**: Deploy as Cloud Run services
- **Azure Container Instances**: Deploy to ACI
- **Kubernetes**: Use Kubernetes manifests

### CI/CD Integration
```yaml
# Example GitHub Actions workflow
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to production
        run: |
          docker-compose up --build -d
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Check what's using the port
netstat -tulpn | grep :8080

# Kill the process
sudo kill -9 <PID>

# Or change ports in docker-compose.yml
```

#### 2. Database Connection Issues
```bash
# Check database logs
docker-compose logs db

# Test database connection
docker-compose exec backend python -c "from utils.database import get_db_connection; print(get_db_connection())"
```

#### 3. Frontend Not Loading
```bash
# Check frontend logs
docker-compose logs frontend

# Test nginx configuration
docker-compose exec frontend nginx -t
```

#### 4. Environment Variables Not Loading
```bash
# Check if .env file exists
ls -la backend/.env

# Verify environment variables
docker-compose exec backend env | grep DATABASE
```

### Debug Commands
```bash
# Enter container shell
docker-compose exec backend bash
docker-compose exec frontend sh

# Check container resources
docker-compose exec backend top
docker-compose exec frontend top

# View container configuration
docker-compose config
```

## 📈 Scaling

### Horizontal Scaling
```bash
# Scale backend services
docker-compose up --scale backend=3

# Use load balancer
# Add nginx load balancer configuration
```

### Vertical Scaling
```yaml
# In docker-compose.yml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
```

## 🔧 Maintenance

### Regular Maintenance
```bash
# Update images
docker-compose pull
docker-compose up --build -d

# Clean up unused resources
docker system prune -f

# Backup volumes
docker run --rm -v academia_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_backup.tar.gz -C /data .
```

### Monitoring
- **Health Checks**: Built-in health monitoring
- **Logs**: Centralized logging with Docker
- **Metrics**: Resource usage monitoring
- **Alerts**: Set up alerts for service failures

## 📚 Additional Resources

### Documentation
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Nginx Configuration](https://nginx.org/en/docs/)

### Tools
- **Docker Desktop**: GUI for container management
- **Portainer**: Web-based container management
- **Docker Compose UI**: Web interface for Docker Compose

---

This Docker setup provides a robust, scalable, and production-ready containerization solution for the AcademiaVeritas application. The configuration is optimized for both development and production environments, with comprehensive monitoring, security, and performance features.

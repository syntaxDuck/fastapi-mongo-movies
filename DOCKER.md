# FastAPI MongoDB Movies - Docker Setup

This directory contains Docker configuration files to containerize the backend and frontend services separately.

## 🐳 Docker Files Overview

### Backend Dockerfile
- **File**: `Dockerfile.backend`
- **Purpose**: Containerizes the FastAPI Python backend
- **Base Image**: Python 3.12-slim
- **Features**: 
  - Multi-stage build with uv package manager
  - Health checks
  - Optimized for production
  - Logs volume mounting

### Frontend Dockerfile  
- **File**: `Dockerfile.frontend`
- **Purpose**: Containerizes the React frontend with nginx
- **Base Image**: Node.js 18-alpine (build), nginx:alpine (production)
- **Features**:
  - Multi-stage build for smaller production image
  - nginx reverse proxy configuration
  - Static asset optimization
  - Security headers

## 🚀 Quick Start

### Development Environment
```bash
# Copy environment file and update with your values
cp .env.docker .env

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Environment
```bash
# Use production compose file
docker-compose -f docker-compose.prod.yml up -d

# Scale services if needed
docker-compose -f docker-compose.prod.yml up -d --scale backend=2
```

## 📁 Environment Variables

Create `.env` file based on `.env.docker`:

```bash
# Required
DB_USER=your_mongodb_username
DB_PASS=your_mongodb_password

# Optional
DB_HOST=mongodb
MONGODB_TLS=true
LOG_LEVEL=INFO
```

## 🔧 Docker Compose Services

### Services Included:
1. **backend**: FastAPI application (port 8000)
2. **frontend**: React application with nginx (port 3000/80)
3. **mongodb**: MongoDB database (port 27017)

### Networks:
- **movies-network**: Internal network for service communication

### Volumes:
- **mongodb_data**: Persistent MongoDB data
- **./logs**: Application logs

## 🌐 Access Points

### Development:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **MongoDB**: localhost:27017

### Production:
- **Frontend**: http://localhost (port 80)
- **Backend API**: http://localhost:8000
- **HTTPS**: Port 443 (configure SSL certificates)

## 🛠️ Build Commands

### Backend Only:
```bash
# Build backend image
docker build -f Dockerfile.backend -t fastapi-movies-backend .

# Run backend container
docker run -p 8000:8000 fastapi-movies-backend
```

### Frontend Only:
```bash
# Build frontend image
docker build -f Dockerfile.frontend -t fastapi-movies-frontend ./frontend

# Run frontend container
docker run -p 80:80 fastapi-movies-frontend
```

### Production Build:
```bash
# Build and tag for production
docker build -f Dockerfile.backend -t fastapi-movies-backend:latest .
docker build -f Dockerfile.frontend -t fastapi-movies-frontend:latest ./frontend

# Push to registry (optional)
docker push your-registry/fastapi-movies-backend:latest
docker push your-registry/fastapi-movies-frontend:latest
```

## 🔍 Health Checks

All containers include health checks:
- **Backend**: `/docs` endpoint availability
- **Frontend**: Root endpoint availability  
- **MongoDB**: Database connectivity

Monitor health:
```bash
docker-compose ps
docker inspect fastapi-movies-backend
```

## 📊 Monitoring & Logs

### View Logs:
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend
docker-compose logs frontend
docker-compose logs mongodb

# Follow logs
docker-compose logs -f backend
```

### Resource Monitoring:
```bash
# Container stats
docker stats

# Resource usage
docker-compose top
```

## 🔧 Development Workflow

### Local Development with Docker:
```bash
# Backend in container, frontend locally
docker-compose up -d backend mongodb

# Frontend in container, backend locally  
docker-compose up -d frontend mongodb

# Rebuild specific service
docker-compose up -d --build backend
```

### Production Deployment:
```bash
# Deploy to production
docker-compose -f docker-compose.prod.yml up -d

# Update specific service
docker-compose -f docker-compose.prod.yml up -d --build frontend

# Backup volumes
docker run --rm -v mongodb_data:/data -v $(pwd):/backup alpine tar czf /backup/mongodb-backup.tar.gz -C /data .
```

## 🔒 Security Considerations

### Production Security:
- MongoDB uses authentication
- Services run in isolated network
- nginx includes security headers
- No shell access in production containers
- Resource limits configured

### Environment Security:
- Use `.env` files (don't commit secrets)
- Rotate MongoDB passwords regularly
- Use external MongoDB for production if possible

## 🐛 Troubleshooting

### Common Issues:

**Port Conflicts:**
```bash
# Check port usage
netstat -tulpn | grep :8000
netstat -tulpn | grep :3000

# Change ports in docker-compose.yml
```

**Connection Issues:**
```bash
# Check network connectivity
docker network ls
docker network inspect fastapi-mongo-movies_movies-network

# Restart services
docker-compose restart
```

**Build Failures:**
```bash
# Clean build cache
docker system prune -a
docker-compose down --rmi all

# Rebuild without cache
docker-compose build --no-cache
```

**Volume Issues:**
```bash
# Check volume permissions
ls -la logs/
chmod 755 logs/

# Inspect volumes
docker volume ls
docker volume inspect mongodb_data
```

## 🚀 Production Considerations

### For Production Use:
1. **External MongoDB**: Use cloud database service
2. **Load Balancer**: Configure nginx or external LB
3. **SSL/TLS**: Add HTTPS certificates
4. **Monitoring**: Add Prometheus/Grafana
5. **Backup**: Regular database backups
6. **Scaling**: Use Docker Swarm or Kubernetes
7. **CI/CD**: GitHub Actions or similar pipeline

### Environment-Specific Changes:
```bash
# Production environment variables
DB_HOST=your-production-mongodb.com
LOG_TO_CONSOLE=false
LOG_LEVEL=WARNING

# Frontend production API URL
REACT_APP_API_URL=https://api.yourdomain.com
```
#!/bin/bash

# Docker deployment script for FastAPI MongoDB Movies

set -e

echo "🐳 FastAPI MongoDB Movies - Docker Deployment"
echo "============================================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.docker .env
    echo "📝 Please edit .env file with your MongoDB credentials and run again."
    exit 1
fi

# Parse arguments
ENVIRONMENT="dev"
BUILD=false
DOWN=false
LOGS=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --prod)
            ENVIRONMENT="prod"
            shift
            ;;
        --build)
            BUILD=true
            shift
            ;;
        --down)
            DOWN=true
            shift
            ;;
        --logs)
            LOGS=true
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --prod     Use production configuration"
            echo "  --build    Force rebuild of images"
            echo "  --down     Stop and remove containers"
            echo "  --logs     Show logs"
            echo "  --help     Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Stop containers if requested
if [ "$DOWN" = true ]; then
    echo "🛑 Stopping and removing containers..."
    if [ "$ENVIRONMENT" = "prod" ]; then
        docker-compose -f docker-compose.prod.yml down -v
    else
        docker-compose down -v
    fi
    echo "✅ Containers stopped and removed"
    exit 0
fi

# Show logs if requested
if [ "$LOGS" = true ]; then
    echo "📋 Showing logs..."
    if [ "$ENVIRONMENT" = "prod" ]; then
        docker-compose -f docker-compose.prod.yml logs -f
    else
        docker-compose logs -f
    fi
    exit 0
fi

# Build and start containers
echo "🚀 Starting $ENVIRONMENT environment..."

if [ "$ENVIRONMENT" = "prod" ]; then
    COMPOSE_FILE="docker-compose.prod.yml"
    echo "📦 Using production configuration..."
else
    COMPOSE_FILE="docker-compose.yml"
    echo "📦 Using development configuration..."
fi

# Build images if requested
if [ "$BUILD" = true ]; then
    echo "🔨 Building images..."
    docker-compose -f $COMPOSE_FILE build --no-cache
fi

# Start services
echo "🌟 Starting services..."
docker-compose -f $COMPOSE_FILE up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service health
echo "🔍 Checking service health..."

if docker-compose -f $COMPOSE_FILE ps | grep -q "Up"; then
    echo "✅ Services are running!"
    
    # Show service URLs
    echo ""
    echo "🌐 Service URLs:"
    if [ "$ENVIRONMENT" = "prod" ]; then
        echo "   Frontend: http://localhost"
    else
        echo "   Frontend: http://localhost:3000"
    fi
    echo "   Backend API: http://localhost:8000"
    echo "   API Docs: http://localhost:8000/docs"
    echo "   MongoDB: localhost:27017"
    echo ""
    echo "📋 To view logs: $0 --logs"
    echo "🛑 To stop services: $0 --down"
else
    echo "❌ Some services failed to start!"
    echo "📋 Check logs: docker-compose -f $COMPOSE_FILE logs"
    exit 1
fi
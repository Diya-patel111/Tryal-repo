#!/bin/bash

# AcademiaVeritas Docker Startup Script
# This script provides easy commands to manage the containerized application

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Function to check if .env file exists
check_env() {
    if [ ! -f "./backend/.env" ]; then
        print_warning ".env file not found. Creating from .env.example..."
        if [ -f "./backend/.env.example" ]; then
            cp ./backend/.env.example ./backend/.env
            print_warning "Please update the .env file with your actual values before running the application."
        else
            print_error ".env.example file not found. Please create a .env file manually."
            exit 1
        fi
    fi
}

# Function to start the application
start_app() {
    print_status "Starting AcademiaVeritas application..."
    check_docker
    check_env
    
    # Build and start containers
    docker-compose up --build -d
    
    print_success "Application started successfully!"
    print_status "Services available at:"
    echo "  - Frontend: http://localhost:8080"
    echo "  - Backend API: http://localhost:5001"
    echo "  - Database: localhost:5432"
    echo "  - Redis: localhost:6379"
    echo ""
    print_status "To view logs: docker-compose logs -f"
    print_status "To stop: docker-compose down"
}

# Function to start development environment
start_dev() {
    print_status "Starting AcademiaVeritas development environment..."
    check_docker
    check_env
    
    # Build and start development containers
    docker-compose -f docker-compose.dev.yml up --build -d
    
    print_success "Development environment started successfully!"
    print_status "Services available at:"
    echo "  - Backend API: http://localhost:5002"
    echo "  - Database: localhost:5433"
    echo "  - Redis: localhost:6380"
    echo ""
    print_status "To view logs: docker-compose -f docker-compose.dev.yml logs -f"
    print_status "To stop: docker-compose -f docker-compose.dev.yml down"
}

# Function to stop the application
stop_app() {
    print_status "Stopping AcademiaVeritas application..."
    docker-compose down
    print_success "Application stopped successfully!"
}

# Function to stop development environment
stop_dev() {
    print_status "Stopping AcademiaVeritas development environment..."
    docker-compose -f docker-compose.dev.yml down
    print_success "Development environment stopped successfully!"
}

# Function to show logs
show_logs() {
    if [ "$1" = "dev" ]; then
        docker-compose -f docker-compose.dev.yml logs -f
    else
        docker-compose logs -f
    fi
}

# Function to clean up
cleanup() {
    print_status "Cleaning up Docker resources..."
    docker-compose down -v
    docker-compose -f docker-compose.dev.yml down -v
    docker system prune -f
    print_success "Cleanup completed!"
}

# Function to show status
show_status() {
    print_status "Checking application status..."
    echo ""
    echo "Production containers:"
    docker-compose ps
    echo ""
    echo "Development containers:"
    docker-compose -f docker-compose.dev.yml ps
}

# Function to show help
show_help() {
    echo "AcademiaVeritas Docker Management Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start       Start the production application"
    echo "  dev         Start the development environment"
    echo "  stop        Stop the production application"
    echo "  stop-dev    Stop the development environment"
    echo "  logs        Show logs for production (use 'logs dev' for development)"
    echo "  status      Show status of all containers"
    echo "  cleanup     Clean up all Docker resources"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start              # Start production environment"
    echo "  $0 dev                # Start development environment"
    echo "  $0 logs               # Show production logs"
    echo "  $0 logs dev           # Show development logs"
    echo "  $0 cleanup            # Clean up everything"
}

# Main script logic
case "${1:-help}" in
    start)
        start_app
        ;;
    dev)
        start_dev
        ;;
    stop)
        stop_app
        ;;
    stop-dev)
        stop_dev
        ;;
    logs)
        show_logs "$2"
        ;;
    status)
        show_status
        ;;
    cleanup)
        cleanup
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac

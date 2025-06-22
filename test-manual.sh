#!/bin/bash

echo "🧪 Testing Daily IT News manually..."
echo "==================================="

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please run ./start.sh first."
    exit 1
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "🐳 Running main container manually..."
docker-compose exec daily-it-news python /app/app/main.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Manual test completed successfully!"
    echo "📧 Check your email for the IT news"
    echo "📁 Check logs/ directory for the saved file"
else
    echo ""
    echo "❌ Manual test failed. Check the error messages above."
    exit 1
fi 
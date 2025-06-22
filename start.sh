#!/bin/bash

echo "🚀 Daily IT News Automation - Setup & Start"
echo "=========================================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "✅ .env file created!"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env file with your actual credentials:"
    echo "   - OpenAI API key"
    echo "   - Email settings (SMTP server, username, password)"
    echo ""
    echo "After editing .env, run this script again."
    exit 0
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "🐳 Building and starting Docker containers..."
docker-compose up -d --build

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Daily IT News Automation is now running!"
    echo ""
    echo "📊 Useful commands:"
    echo "   View scheduler logs: docker-compose logs -f scheduler"
    echo "   View main app logs: docker-compose logs daily-it-news"
    echo "   Stop service: docker-compose down"
    echo "   Restart service: docker-compose restart"
    echo "   Test manually: docker-compose run --rm daily-it-news"
    echo ""
    echo "📅 The service will send IT news every day at 07:00"
    echo "📁 Logs are saved in the ./logs/ directory"
    echo "🔄 Scheduler runs continuously and will restart automatically"
else
    echo "❌ Failed to start the service. Check the error messages above."
    exit 1
fi 
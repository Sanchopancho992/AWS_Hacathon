#!/bin/bash

# Hong Kong Tourism AI - Setup Script
# This script sets up the complete development environment

echo "🚀 Setting up Hong Kong Tourism AI Project..."

# Check if required tools are installed
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ $1 is not installed. Please install it first."
        exit 1
    fi
}

echo "📋 Checking prerequisites..."
check_command "python"
check_command "node"
check_command "npm"

# Setup Backend
echo "🔧 Setting up backend..."
cd backend

# Create virtual environment (optional but recommended)
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating backend .env file..."
    cp .env.example .env
    echo "📝 Please edit backend/.env with your API keys"
fi

cd ..

# Setup Frontend
echo "🎨 Setting up frontend..."
cd frontend

# Install Node dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating frontend .env file..."
    echo "REACT_APP_API_URL=http://localhost:8000" > .env
fi

cd ..

echo "✅ Setup complete!"
echo ""
echo "🚀 To start the application:"
echo "  1. Backend: cd backend && python main.py"
echo "  2. Frontend: cd frontend && npm start"
echo ""
echo "📝 Don't forget to:"
echo "  1. Add your Google API key to backend/.env"
echo "  2. Configure AWS credentials (optional)"
echo ""
echo "🌐 Access the application at http://localhost:3000"

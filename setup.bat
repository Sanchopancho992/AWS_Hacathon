@echo off
REM Hong Kong Tourism AI - Windows Setup Script

echo 🚀 Setting up Hong Kong Tourism AI Project...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python first.
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js first.
    exit /b 1
)

REM Setup Backend
echo 🔧 Setting up backend...
cd backend

REM Create virtual environment (optional but recommended)
if not exist "venv" (
    echo 📦 Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install Python dependencies
echo 📦 Installing Python dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo ⚙️  Creating backend .env file...
    copy .env.example .env
    echo 📝 Please edit backend\.env with your API keys
)

cd ..

REM Setup Frontend
echo 🎨 Setting up frontend...
cd frontend

REM Install Node dependencies
echo 📦 Installing Node.js dependencies...
npm install

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo ⚙️  Creating frontend .env file...
    echo REACT_APP_API_URL=http://localhost:8000 > .env
)

cd ..

echo ✅ Setup complete!
echo.
echo 🚀 To start the application:
echo   1. Backend: cd backend ^&^& python main.py
echo   2. Frontend: cd frontend ^&^& npm start
echo.
echo 📝 Don't forget to:
echo   1. Add your Google API key to backend\.env
echo   2. Configure AWS credentials (optional)
echo.
echo 🌐 Access the application at http://localhost:3000

pause

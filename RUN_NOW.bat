@echo off
REM FARM Stack Blog - Quick Start Script (Windows)
REM This script sets up and runs the application

echo ==========================================
echo FARM Stack Blog - Quick Start
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed. Please install Node.js 18 or higher.
    pause
    exit /b 1
)

echo [OK] Python and Node.js are installed
echo.

REM Setup Backend
echo Setting up Backend...
cd backend

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Check if .env exists
if not exist ".env" (
    echo ERROR: .env file not found in backend\
    echo Please create backend\.env with your MongoDB URL:
    echo MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/blog
    pause
    exit /b 1
)

echo [OK] Backend setup complete
echo.

REM Setup Frontend
echo Setting up Frontend...
cd ..\frontend

REM Install dependencies
if not exist "node_modules" (
    echo Installing Node dependencies...
    call npm install
)

REM Check if .env.local exists
if not exist ".env.local" (
    echo Creating .env.local...
    (
        echo NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
    ) > .env.local
)

echo [OK] Frontend setup complete
echo.

echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo To run the application:
echo.
echo Terminal 1 - Backend:
echo   cd backend
echo   venv\Scripts\activate.bat
echo   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
echo.
echo Terminal 2 - Frontend:
echo   cd frontend
echo   npm run dev
echo.
echo Then open: http://localhost:3000
echo.
echo ==========================================
echo.
pause

@echo off
REM AI Nexus - Desktop App Build Script (Windows)
REM Builds native desktop application

echo ======================================
echo   AI Nexus Desktop App Builder
echo ======================================
echo.

REM Check Node.js
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js not found. Please install Node.js 16+
    pause
    exit /b 1
)

echo [OK] Node.js version:
node --version

REM Install dependencies if needed
if not exist "node_modules" (
    echo [INFO] Installing dependencies...
    call npm install
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Parse argument
set BUILD_TARGET=%1
if "%BUILD_TARGET%"=="" set BUILD_TARGET=win

if "%BUILD_TARGET%"=="win" (
    echo [BUILD] Building for Windows...
    call npm run build:win
    echo [DONE] Windows build complete!
    echo [INFO] Output: dist\*.exe
) else if "%BUILD_TARGET%"=="all" (
    echo [BUILD] Building for all platforms...
    call npm run build:all
    echo [DONE] All builds complete!
    echo [INFO] Output: dist\*
) else if "%BUILD_TARGET%"=="current" (
    echo [BUILD] Building for current platform...
    call npm run build
    echo [DONE] Build complete!
    echo [INFO] Output: dist\*
) else (
    echo Usage: build.bat [win^|all^|current]
    echo.
    echo Examples:
    echo   build.bat       # Build for Windows
    echo   build.bat win   # Build for Windows
    echo   build.bat all   # Build for all platforms
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Build successful!
echo.
echo To run the app:
echo   npm start
echo.
pause

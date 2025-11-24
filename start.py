#!/usr/bin/env python3
"""
AI Nexus - Cross-platform Launcher
Works on Windows, Linux, and macOS
"""
import os
import sys
import subprocess
import time
import platform
import socket
from pathlib import Path

# Colors for terminal output
class Colors:
    if platform.system() == "Windows":
        # Windows color support
        os.system("color")
    
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_color(text, color=Colors.OKGREEN):
    """Print colored text"""
    print(f"{color}{text}{Colors.ENDC}")

def print_banner():
    """Print startup banner"""
    print_color("=" * 60, Colors.HEADER)
    print_color("🤖 AI Nexus - Starting...", Colors.HEADER)
    print_color("=" * 60, Colors.HEADER)

def check_python_version():
    """Ensure Python 3.8+"""
    if sys.version_info < (3, 8):
        print_color("❌ Python 3.8+ required!", Colors.FAIL)
        sys.exit(1)
    print_color(f"✅ Python {sys.version.split()[0]}", Colors.OKGREEN)

def setup_virtualenv():
    """Create and activate virtual environment"""
    venv_dir = "venv"
    venv_path = Path(venv_dir)
    
    # Determine venv python/pip paths based on OS
    if platform.system() == "Windows":
        python_exe = venv_path / "Scripts" / "python.exe"
        pip_exe = venv_path / "Scripts" / "pip.exe"
        activate_cmd = str(venv_path / "Scripts" / "activate.bat")
    else:
        python_exe = venv_path / "bin" / "python"
        pip_exe = venv_path / "bin" / "pip"
        activate_cmd = f"source {venv_path / 'bin' / 'activate'}"
    
    # Create venv if it doesn't exist
    if not venv_path.exists():
        print_color("📦 Creating virtual environment...", Colors.OKCYAN)
        try:
            subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)
            print_color("✅ Virtual environment created", Colors.OKGREEN)
        except subprocess.CalledProcessError as e:
            print_color(f"❌ Failed to create venv: {e}", Colors.FAIL)
            sys.exit(1)
    else:
        print_color("✅ Virtual environment exists", Colors.OKGREEN)
    
    return python_exe, pip_exe

def install_dependencies(pip_exe):
    """Install Python dependencies"""
    print_color("📥 Installing dependencies...", Colors.OKCYAN)
    try:
        subprocess.run([str(pip_exe), "install", "-q", "-r", "requirements.txt"], check=True)
        print_color("✅ Dependencies installed", Colors.OKGREEN)
    except subprocess.CalledProcessError as e:
        print_color(f"⚠️  Warning: Some dependencies may have failed: {e}", Colors.WARNING)
        # Continue anyway

def ensure_directories():
    """Create required directories"""
    dirs = ["har_and_cookies", "memory_db", "temp_home"]
    for d in dirs:
        Path(d).mkdir(exist_ok=True)
    print_color("✅ Directories initialized", Colors.OKGREEN)

def check_port_available(port):
    """Check if a port is available"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result != 0

def start_services(python_exe):
    """Start API and Streamlit services"""
    processes = []
    
    # Start API server
    print_color("🚀 Starting API server (port 8000)...", Colors.OKCYAN)
    if not check_port_available(8000):
        print_color("⚠️  Port 8000 already in use", Colors.WARNING)
    else:
        api_process = subprocess.Popen(
            [str(python_exe), "-m", "uvicorn", "api:app", 
             "--host", "0.0.0.0", "--port", "8000"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        processes.append(("API", api_process))
        time.sleep(2)
        print_color("✅ API server started", Colors.OKGREEN)
    
    # Start Streamlit
    print_color("🎨 Starting Streamlit app (port 8501)...", Colors.OKCYAN)
    if not check_port_available(8501):
        print_color("⚠️  Port 8501 already in use", Colors.WARNING)
    else:
        streamlit_process = subprocess.Popen(
            [str(python_exe), "-m", "streamlit", "run", "app.py",
             "--server.headless=true"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        processes.append(("Streamlit", streamlit_process))
        time.sleep(3)
        print_color("✅ Streamlit app started", Colors.OKGREEN)
    
    return processes

def print_access_info():
    """Print access information"""
    print()
    print_color("=" * 60, Colors.HEADER)
    print_color("✅ AI Nexus is running!", Colors.OKGREEN)
    print_color("=" * 60, Colors.HEADER)
    print()
    print_color("📍 Choose your interface:", Colors.OKBLUE)
    
    # Get absolute path for local files
    current_dir = Path.cwd().absolute()
    landing_page = f"file:///{current_dir / 'index.html'}".replace("\\", "/")
    chat_page = f"file:///{current_dir / 'examples' / 'chat-full.html'}".replace("\\", "/")
    
    print(f"   Landing Page: {landing_page}")
    print(f"   Desktop App:  http://localhost:8501")
    print(f"   Web Chat:     {chat_page}")
    print(f"   API Docs:     http://localhost:8000/docs")
    print()
    print_color("Press Ctrl+C to stop all services", Colors.WARNING)
    print()

def main():
    """Main launcher function"""
    try:
        print_banner()
        check_python_version()
        python_exe, pip_exe = setup_virtualenv()
        install_dependencies(pip_exe)
        ensure_directories()
        
        # Initialize config
        try:
            sys.path.insert(0, str(Path.cwd()))
            import config
            config.ensure_directories()
            config.validate_config()
        except ImportError:
            print_color("ℹ️  Config module not found, using defaults", Colors.WARNING)
        
        processes = start_services(python_exe)
        print_access_info()
        
        # Wait for Ctrl+C
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print()
            print_color("🛑 Stopping services...", Colors.WARNING)
            for name, proc in processes:
                proc.terminate()
                print_color(f"   Stopped {name}", Colors.OKGREEN)
            print()
            print_color("👋 AI Nexus stopped", Colors.OKGREEN)
    
    except Exception as e:
        print_color(f"❌ Error: {e}", Colors.FAIL)
        sys.exit(1)

if __name__ == "__main__":
    main()

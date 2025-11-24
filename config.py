"""
Configuration module for AI Nexus - Centralized settings for portability
"""
import os
from pathlib import Path
from typing import Optional

# Base directory - works across all environments
BASE_DIR = Path(__file__).parent.absolute()

# Data directories
MEMORY_DB_PATH = os.getenv("MEMORY_DB_PATH", str(BASE_DIR / "memory_db"))
HAR_COOKIES_PATH = os.getenv("HAR_COOKIES_PATH", str(BASE_DIR / "har_and_cookies"))
CUSTOM_PROVIDERS_FILE = os.getenv("CUSTOM_PROVIDERS_FILE", str(BASE_DIR / "custom_providers.json"))

# Network configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost")
OLLAMA_PORT = int(os.getenv("OLLAMA_PORT", "11434"))
OLLAMA_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}"

API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

STREAMLIT_HOST = os.getenv("STREAMLIT_HOST", "0.0.0.0")
STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", "8501"))

# API Keys (with validation)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY", "")

# Timeouts
API_TIMEOUT = float(os.getenv("API_TIMEOUT", "30.0"))
OLLAMA_TIMEOUT = float(os.getenv("OLLAMA_TIMEOUT", "60.0"))

# Feature flags
ENABLE_MEMORY = os.getenv("ENABLE_MEMORY", "true").lower() == "true"
ENABLE_G4F = os.getenv("ENABLE_G4F", "true").lower() == "true"

# Create required directories
def ensure_directories():
    """Create required directories if they don't exist"""
    Path(MEMORY_DB_PATH).mkdir(parents=True, exist_ok=True)
    Path(HAR_COOKIES_PATH).mkdir(parents=True, exist_ok=True)
    print(f"✅ Directories initialized:")
    print(f"   Memory DB: {MEMORY_DB_PATH}")
    print(f"   HAR/Cookies: {HAR_COOKIES_PATH}")

def validate_config():
    """Validate configuration and warn about missing keys"""
    warnings = []
    
    if not OPENAI_API_KEY:
        warnings.append("⚠️  OPENAI_API_KEY not set - OpenAI features will use free fallback")
    if not ANTHROPIC_API_KEY:
        warnings.append("⚠️  ANTHROPIC_API_KEY not set - Anthropic features will use free fallback")
    if not GOOGLE_API_KEY:
        warnings.append("⚠️  GOOGLE_API_KEY not set - Google features will use free fallback")
    if not PERPLEXITY_API_KEY:
        warnings.append("⚠️  PERPLEXITY_API_KEY not set - Perplexity features will use free fallback")
    
    if warnings:
        print("\n" + "\n".join(warnings))
        print("💡 Free Web (g4f) will be used as fallback for missing API keys\n")
    
    print(f"🌐 Network Configuration:")
    print(f"   Ollama: {OLLAMA_URL}")
    print(f"   API Server: {API_HOST}:{API_PORT}")
    print(f"   Streamlit: {STREAMLIT_HOST}:{STREAMLIT_PORT}")

def get_ollama_generate_url():
    """Get Ollama generate endpoint URL"""
    return f"{OLLAMA_URL}/api/generate"

def get_ollama_tags_url():
    """Get Ollama tags endpoint URL"""
    return f"{OLLAMA_URL}/api/tags"

if __name__ == "__main__":
    print("AI Nexus Configuration")
    print("=" * 60)
    ensure_directories()
    validate_config()

# AI Nexus - Portability and Deployment Guide

## 🌍 Cross-Platform Support

AI Nexus now works seamlessly across **Windows**, **Linux**, and **macOS** with zero modification!

## 🚀 Quick Start (Any Platform)

### Option 1: Using Python Launcher (Recommended)
```bash
python3 start.py
```

### Option 2: Platform-Specific Scripts

**Linux/macOS:**
```bash
./run.sh
```

**Windows:**
```cmd
start.bat
```
Or double-click `start.bat`

## ⚙️ Configuration

All settings are controlled via environment variables for maximum portability.

### 1. Copy the Example Configuration
```bash
cp .env.example .env
```

### 2. Edit .env File
```bash
# Required only if you want to use paid APIs
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here

# Network configuration (defaults shown)
OLLAMA_HOST=localhost
OLLAMA_PORT=11434
API_PORT=8000
STREAMLIT_PORT=8501
```

## 🐳 Docker Deployment

### Build and Run with Docker Compose
```bash
docker-compose up -d
```

### Access Points (Docker)
- Streamlit App: `http://localhost:8501`
- API Server: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

## ☁️ Cloud/Remote Deployment

### Deploy with Remote Ollama

1. **Setup Ollama on a server:**
```bash
# On your Ollama server
ollama serve --host 0.0.0.0:11434
```

2. **Configure AI Nexus to use remote Ollama:**
```bash
# In .env file
OLLAMA_HOST=192.168.1.100  # Your Ollama server IP
OLLAMA_PORT=11434
```

### Network Access for Mobile/Remote Devices

AI Nexus binds to `0.0.0.0` by default, making it accessible from other devices on your network.

**Find your access URL:**
```bash
python3 diagnose_network.py
```

This will show:
- Your local network IP
- QR code for mobile access
- Port availability status

## 📱 Mobile Access

### Access from Phone/Tablet

1. Ensure AI Nexus is running on your computer
2. Run network diagnostic: `python3 diagnose_network.py`
3. Scan the QR code with your phone or
4. Navigate to: `http://YOUR_IP:8501`

**Note:** Both devices must be on the same network

## 🔧 Environment Variables

### All Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_HOST` | localhost | Ollama server hostname/IP |
| `OLLAMA_PORT` | 11434 | Ollama server port |
| `API_HOST` | 0.0.0.0 | API server bind address |
| `API_PORT` | 8000 | API server port |
| `STREAMLIT_HOST` | 0.0.0.0 | Streamlit bind address |
| `STREAMLIT_PORT` | 8501 | Streamlit port |
| `MEMORY_DB_PATH` | ./memory_db | Vector DB storage path |
| `API_TIMEOUT` | 30.0 | API call timeout (seconds) |
| `OLLAMA_TIMEOUT` | 60.0 | Ollama timeout (seconds) |
| `ENABLE_MEMORY` | true | Enable memory/knowledge base |
| `ENABLE_G4F` | true | Enable free web fallback |

## 🐧 Linux/Unix Specific

### Service Setup (systemd)

Create `/etc/systemd/system/ai-nexus.service`:
```ini
[Unit]
Description=AI Nexus Service
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/Multi-LLM-Aggregator
ExecStart=/usr/bin/python3 /path/to/Multi-LLM-Aggregator/start.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable ai-nexus
sudo systemctl start ai-nexus
```

## 🪟 Windows Specific

### Running as a Service

Use NSSM (Non-Sucking Service Manager):

1. Download NSSM from https://nssm.cc/
2. Install as service:
```cmd
nssm install AILexus "C:\Python310\python.exe" "C:\path\to\start.py"
nssm start AILexus
```

## 🌐 Reverse Proxy Setup

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
    }
}
```

## 🔐 Security Considerations

### For Production Deployment:

1. **Use environment variables for secrets** (never commit .env)
2. **Enable HTTPS** with Let's Encrypt or similar
3. **Firewall rules** - only expose necessary ports
4. **Authentication** - consider adding auth layer for public deployments

## 🛠️ Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows

# Kill the process or change port in .env
API_PORT=8001
```

### Cannot Connect to Ollama
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Try starting Ollama
ollama serve
```

### Module Not Found Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

## 📊 Performance Tuning

### For Large Scale Deployments:

```bash
# Increase worker processes in .env
UVICORN_WORKERS=4

# Adjust timeouts for slower networks
API_TIMEOUT=60.0
OLLAMA_TIMEOUT=120.0
```

## 🚢 Kubernetes Deployment

See `k8s/` directory for Kubernetes manifests (coming soon)

## 📝 Migration from Old Setup

If you were using hard-coded localhost:
1. No changes needed! Defaults work as before
2. To use remote services, simply set environment variables
3. Old .env files are compatible

## 🆘 Support

- GitHub Issues: https://github.com/your-repo/issues
- Documentation: See `wiki/` directory
- Network Diagnostics: Run `python3 diagnose_network.py`

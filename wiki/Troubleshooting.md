# 🔧 Troubleshooting

Common issues and how to fix them.

## 🚨 Quick Diagnostics

Run these commands to check your setup:

```bash
# Check Python version
python3 --version  # Should be 3.10+

# Check Ollama
ollama list        # Should show your models

# Check dependencies
pip list | grep streamlit
pip list | grep fastapi
```

---

## 🐛 Common Issues

### "ModuleNotFoundError"

**Problem**: Python can't find a required library.

**Solution**:
```bash
# Activate virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### "Ollama 404 Error" or "Model Not Found"

**Problem**: App can't connect to Ollama.

**Solution**:
```bash
# 1. Start Ollama
ollama serve

# 2. Pull a model (in another terminal)
ollama pull llama3

# 3. Verify it's running
curl http://localhost:11434/api/tags
```

### "Port Already in Use"

**Problem**: Port 8501 or 8000 is occupied.

**Solution**:
```bash
# Find what's using the port
lsof -i :8501   # Mac/Linux
netstat -ano | findstr :8501  # Windows

# Kill the process or use different port
streamlit run app.py --server.port 8502
uvicorn api:app --port 8001
```

### "Connection Refused" from Mobile App

**Problem**: Phone can't reach your computer.

**Solutions**:

1. **Check same network**:
   - Phone and computer on same Wi-Fi?

2. **Check firewall**:
   ```bash
   # Mac
   sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /path/to/python
   
   # Linux
   sudo ufw allow 8000/tcp
   
   # Windows
   # Add rule in Windows Defender Firewall
   ```

3. **Verify IP address**:
   ```bash
   # Get your IP
   ip addr show     # Linux
   ipconfig         # Windows  
   ifconfig         # Mac
   ```

---

## 🌐 Discovery Issues

### "No Models Found" in Global Search

**Problem**: Search returns empty.

**Reasons**:
- Model name doesn't exist (e.g., "gemini3" → try "gemini")
- No OpenRouter key for premium search
- Network issues

**Solution**:
```bash
# Test g4f connection
python -c "import g4f; print(dir(g4f.models))"

# Try exact model names:
# - For g4f: gpt_4, gemini, llama_3_1_8b
# - For OpenRouter: need API key
```

### "Test & Add" Fails

**Problem**: Model verification times out.

**Solution**:
- Try a different model
- Check internet connection
- Some models require API keys (OpenRouter)
- Local models: ensure Ollama is running

---

## 🧠 Memory Issues

### "Memory Not Available"

**Problem**: ChromaDB not installed.

**Solution**:
```bash
pip install chromadb sentence-transformers
```

### "Out of Memory" Errors

**Problem**: Too much data in memory.

**Solution**:
```bash
# Clear the database
rm -rf ./memory_db

# Or reduce memory usage
# In app sidebar: Disable "Enable Learning"
```

---

## 📱 Mobile App Issues

### App Won't Load

**Solutions**:
```bash
# Clear Expo cache
npx expo start --clear

# Reinstall dependencies
cd mobile
rm -rf node_modules
npm install
```

### "Cannot Read Property" Errors

**Problem**: API response format changed.

**Solution**:
- Update both desktop and mobile apps
- Clear mobile app cache
- Re-scan QR code

---

## 🐳 Docker Issues

### Build Takes Forever

**Problem**: Downloading large dependencies (PyTorch, etc.).

**Solutions**:
- Use local installation instead (`./run.sh`)
- Use pre-built base images
- Build only once, then `docker-compose up` (without `--build`)

### Container Can't Connect to Ollama

**Problem**: Network isolation in Docker.

**Solution**:
In `docker-compose.yml`:
```yaml
services:
  frontend:
    environment:
      - OLLAMA_HOST=http://ollama:11434  # Use service name
```

---

## 🔑 API Key Issues

### "Invalid API Key"

**Solutions**:
- Check for extra spaces
- Verify key is still active
- Try generating a new key
- Some providers need special format (e.g., `sk-ant-...` for Anthropic)

### Keys Not Saving

**Problem**: Session state reset.

**Solution**:
- Keys are stored in browser session
- Use `.env` file for persistence:
  ```env
  OPENAI_API_KEY=sk-...
  ANTHROPIC_API_KEY=sk-ant-...
  ```

---

## 🧪 Testing Issues

### Tests Fail

**Problem**: Dependency or environment issues.

**Solution**:
```bash
# Reinstall test dependencies
pip install pytest pytest-asyncio

# Run specific test
pytest tests/test_api.py -v

# Run with debugging
pytest tests/ -vv --tb=short
```

---

## 📊 Performance Issues

### Slow Responses

**Solutions**:
1. Use fewer models per query
2. Use faster models (gpt-3.5 vs gpt-4)
3. Disable memory for speed
4. Check network latency

### High CPU Usage

**Solutions**:
1. Limit concurrent queries
2. Use GPU for Ollama if available
3. Reduce synthesis model size

---

## 🆘 Still Need Help?

1. **Check Logs**:
   ```bash
   # Streamlit logs
   # Shown in terminal where you ran "streamlit run app.py"
   
   # FastAPI logs
   # Shown in terminal where you ran "uvicorn api:app"
   ```

2. **Enable Debug Mode**:
   ```bash
   streamlit run app.py --logger.level=debug
   uvicorn api:app --log-level debug
   ```

3. **Create an Issue**:
   - Visit: https://github.com/jimmymannekkattu/Multi-LLM-Aggregator/issues
   - Include:
     - Error message
     - Steps to reproduce
     - Your setup (OS, Python version, etc.)

---

## ⏭️ Next Steps

- **[User Guide](User-Guide)** - Learn proper usage
- **[Installation Guide](Installation-Guide)** - Reinstall cleanly
- **[API Documentation](API-Documentation)** - Understand internals

# End User WebSocket Guide

## 🌐 For End Users - How to Use AI Nexus

### Web Interface (Easiest)

1. **Start the Server** (Admin does this):
   ```bash
   ./run.sh
   ```

2. **Access the Chat**:
   - Open `examples/chat.html` in any web browser
   - OR visit: `file:///path/to/examples/chat.html`

3. **Start Chatting**:
   - Type your question
   - Press Enter or click Send
   - Get AI-powered answers!

### Direct WebSocket Connection

For developers integrating AI Nexus into their apps:

**Endpoint**: `ws://localhost:8000/ws/chat`

**Send**:
```json
{
  "query": "Your question here",
  "online_models": ["ChatGPT (OpenAI)"],
  "offline_models": ["llama3"],
  "use_memory": true
}
```

**Receive** (progressively):
```json
{"status": "processing", "message": "..."}
{"status": "querying", "model": "..."}
{"status": "response", "model": "...", "content": "..."}
{"status": "complete", "final_answer": "...", "individual_responses": {...}}
```

## 🚀 Deployment for Public Access

### Local Network
Users on the same Wi-Fi can access:
- Replace `localhost` with your server IP in `chat.html`
- Example: `ws://192.168.1.100:8000/ws/chat`

### Internet (Advanced)
1. Use a reverse proxy (Nginx/Caddy)
2. Add SSL certificate
3. Update WebSocket URL to `wss://your-domain.com/ws/chat`

## 🔒 Production Considerations

- Add authentication to WebSocket endpoint
- Rate limiting per user
- Connection timeout handling
- Error recovery

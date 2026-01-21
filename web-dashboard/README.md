# SignSpeak Smart Glove - React Dashboard

Real-time web dashboard for monitoring SignSpeak Smart Glove gestures.

## Features

- 🎯 **Real-time Gesture Detection** - Live updates via WebSocket
- 📊 **Confidence Percentage** - Visual confidence indicator
- 💬 **Generated Sentences** - Gemini-powered natural language
- 🌐 **Multi-language Support** - English, Hindi, Marathi
- 🔌 **Device Status** - ESP32 connection monitoring
- ⚡ **Latency Tracking** - Real-time performance metrics
- 🔊 **Text-to-Speech** - Browser-based TTS playback

## Setup Instructions

### Step 1: Install Dependencies

```bash
cd web-dashboard
npm install
```

### Step 2: Start Backend (Terminal 1)

```bash
cd Web
python -m pip install fastapi uvicorn websockets
python backend.py
```

Backend runs on: `http://localhost:8000`

### Step 3: Start React App (Terminal 2)

```bash
cd web-dashboard
npm start
```

React app runs on: `http://localhost:3000`

## Environment Variables

Edit `.env` file to change API URLs:

```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000/ws
```

## API Endpoints

### WebSocket
- **URL**: `ws://localhost:8000/ws`
- **Purpose**: Real-time gesture data streaming
- **Message Format**:
```json
{
  "gesture": "HELLO",
  "confidence": 98.2,
  "sentence": "Hello, how can I help you?",
  "latency_ms": 210,
  "device_status": "CONNECTED"
}
```

### REST API
- **POST** `/set-language` - Change TTS language
  ```json
  { "language": "en" | "hi" | "mr" }
  ```

## Production Build

```bash
npm run build
```

Built files will be in `build/` folder. Configure backend to serve these static files.

## Tech Stack

- **Frontend**: React, CSS3
- **Backend**: FastAPI, WebSockets
- **Communication**: WebSocket (real-time), REST API
- **TTS**: Web Speech API

## Browser Support

- Chrome/Edge (Recommended)
- Firefox
- Safari (limited TTS support)

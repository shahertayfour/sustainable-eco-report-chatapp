# Sustainable Eco Chat App

A microservices-based chat application using Flask backend with Ollama integration and Bootstrap frontend.

## Architecture

```
sustainable-eco-report-chatapp/
├── backend/          # Flask API service
├── frontend/         # Bootstrap web interface
├── shared/           # Shared utilities
├── .env             # Environment configuration
└── README.md
```

## Prerequisites

1. **Ollama**: Install Ollama and download the Llama 3.1 model
   ```bash
   # Install Ollama (visit https://ollama.ai for instructions)
   ollama pull llama3.1
   ```

2. **Python 3.8+**: For the Flask backend
3. **Modern web browser**: For the frontend

## Setup Instructions

### 1. Clone and Setup Environment

```bash
git clone <repository-url>
cd sustainable-eco-report-chatapp
cp .env.example .env
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

### 3. Start Services

**Terminal 1 - Start Ollama:**
```bash
ollama serve
```

**Terminal 2 - Start Backend:**
```bash
cd backend
python app.py
```

**Terminal 3 - Start Frontend:**
```bash
cd frontend
python -m http.server 3000
```

### 4. Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- Health Check: http://localhost:5000/health

## Environment Variables

You can override the Flask port using the `.env` file:

```env
FLASK_PORT=5000          # Default Flask port
FLASK_DEBUG=False        # Debug mode
OLLAMA_URL=http://localhost:11434
MODEL_NAME=llama3.1
```

## API Endpoints

- `GET /health` - Health check
- `POST /chat` - Send message to AI
- `GET /models` - List available Ollama models

## Features

- ✅ Responsive Bootstrap UI
- ✅ Real-time chat interface
- ✅ Ollama Llama 3.1 integration
- ✅ Microservices architecture
- ✅ Environment configuration
- ✅ CORS enabled
- ✅ Error handling
- ✅ Typing indicators

## Development

To modify the Flask port, update the `FLASK_PORT` variable in your `.env` file.
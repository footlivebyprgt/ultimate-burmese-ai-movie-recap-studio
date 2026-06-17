# Installation & Setup Guide

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- FFmpeg (for video processing)
- API Keys:
  - Google Gemini API Key
  - OpenAI API Key (optional, for Whisper transcription)

### Step 1: Clone Repository

```bash
git clone https://github.com/footlivebyprgt/ultimate-burmese-ai-movie-recap-studio.git
cd ultimate-burmese-ai-movie-recap-studio
```

### Step 2: Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install FFmpeg

**On Windows:**
```bash
# Using Chocolatey
choco install ffmpeg

# Or download from https://ffmpeg.org/download.html
```

**On macOS:**
```bash
brew install ffmpeg
```

**On Linux (Ubuntu/Debian):**
```bash
sudo apt-get install ffmpeg
```

### Step 5: Configure API Keys

Create a `.streamlit/secrets.toml` file in your home directory:

```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
OPENAI_API_KEY = "your_openai_api_key_here"
```

**Or** set environment variables:

```bash
export GEMINI_API_KEY="your_gemini_api_key_here"
export OPENAI_API_KEY="your_openai_api_key_here"
```

### Step 6: Run Application

```bash
streamlit run streamlit_app.py
```

The application will open in your browser at `http://localhost:8501`

---

## 📋 Detailed Setup Instructions

### Getting API Keys

#### Google Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the API key
4. Add to `.streamlit/secrets.toml` or environment variable

#### OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Click "Create new secret key"
3. Copy the API key
4. Add to `.streamlit/secrets.toml` or environment variable

### Streamlit Configuration

Create `.streamlit/config.toml` in your home directory for custom settings:

```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[client]
showErrorDetails = true
toolbarMode = "minimal"

[server]
maxUploadSize = 500
```

---

## 🔧 Troubleshooting

### Issue: "MoviePy is not installed"

**Solution:**
```bash
pip install moviepy
```

### Issue: "FFmpeg not found"

**Solution:**
Make sure FFmpeg is installed and added to PATH. Test with:
```bash
ffmpeg -version
```

### Issue: "API Key is invalid"

**Solution:**
- Verify API key is correct
- Check that API key has not expired
- Ensure API key is properly formatted (no extra spaces)

### Issue: "Streamlit not found"

**Solution:**
```bash
pip install streamlit
```

### Issue: "Port 8501 is already in use"

**Solution:**
```bash
streamlit run streamlit_app.py --server.port 8502
```

---

## 📦 Project Structure

```
ultimate-burmese-ai-movie-recap-studio/
├── streamlit_app.py              # Main entry point
├── streamlit_app_main.py         # Integrated application
├── streamlit_app_phase1.py       # Phase 1: Upload Content
├── streamlit_app_phase2.py       # Phase 2: Generate Script
├── streamlit_app_phase3.py       # Phase 3: Create Voiceover
├── streamlit_app_phase4.py       # Phase 4: Assemble Video
├── streamlit_app_phase5.py       # Phase 5: Deploy & Manage
├── utils.py                      # Utility functions
├── ai_services.py                # AI services (Whisper, Gemini)
├── tts_services.py               # Text-to-Speech services
├── video_services.py             # Video processing services
├── project_management.py         # Project management
├── requirements.txt              # Python dependencies
├── .streamlit/
│   └── config.toml              # Streamlit configuration
├── README.md                     # Project documentation
├── INSTALLATION.md              # This file
└── LICENSE                      # License file
```

---

## 🐳 Docker Setup (Optional)

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8501

# Run application
CMD ["streamlit", "run", "streamlit_app.py"]
```

### Build and Run Docker Container

```bash
# Build image
docker build -t ultimate-recap-studio .

# Run container
docker run -p 8501:8501 \
  -e GEMINI_API_KEY="your_key" \
  -e OPENAI_API_KEY="your_key" \
  ultimate-recap-studio
```

---

## 🌐 Deployment Options

### Streamlit Cloud

1. Push code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click "New app"
4. Select your repository
5. Add secrets in "Advanced settings"
6. Deploy

### Heroku

```bash
# Create Procfile
echo "web: streamlit run streamlit_app.py --logger.level=error" > Procfile

# Create runtime.txt
echo "python-3.11.0" > runtime.txt

# Deploy
git push heroku main
```

### AWS, Google Cloud, Azure

See respective documentation for Streamlit deployment.

---

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google Generative AI Documentation](https://ai.google.dev/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [MoviePy Documentation](https://zulko.github.io/moviepy/)
- [Edge TTS Documentation](https://github.com/rany2/edge-tts)

---

## 💬 Support

For issues or questions:
1. Check [GitHub Issues](https://github.com/footlivebyprgt/ultimate-burmese-ai-movie-recap-studio/issues)
2. Create a new issue with detailed description
3. Include error messages and system information

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

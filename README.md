# 🎬 Ultimate Burmese AI Movie Recap Studio

Transform your movies into engaging Burmese AI-generated recaps with a single click!

## 🌟 Features

- **Multiple Input Methods:**
  - Upload local video files (MP4, MKV, MOV)
  - Fetch videos from YouTube
  - Upload movie scripts or documents (PDF, DOCX, TXT, SRT)

- **AI-Powered Script Generation:**
  - Automatic audio transcription using OpenAI Whisper
  - AI script generation using Google Gemini AI
  - Customizable script editing interface

- **Professional Voiceover Production:**
  - Multi-language support (Burmese, English, Thai, etc.)
  - Male/Female voice selection
  - Parallel TTS generation for faster processing
  - Automatic duration validation and speed adjustment

- **Video Assembly & Branding:**
  - Combine voiceover with original video
  - Add custom logos/watermarks
  - Burn-in Burmese subtitles
  - Multiple aspect ratio support (16:9, 9:16, 1:1)

## 📋 Project Structure

```
ultimate-recap-studio/
├── streamlit_app.py          # Main Streamlit application
├── utils.py                  # Utility functions (validation, extraction, etc.)
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── config.toml          # Streamlit configuration
└── README.md                # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip or conda package manager
- API Keys:
  - Google Gemini API Key (from https://aistudio.google.com/app/apikey)
  - OpenAI API Key (from https://platform.openai.com/api-keys)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/footlivebyprgt/ultimate-recap-studio.git
cd ultimate-recap-studio
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Configuration

Create a `.streamlit/secrets.toml` file in your home directory:

```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
OPENAI_API_KEY = "your_openai_api_key_here"
```

### Running the Application

```bash
streamlit run streamlit_app.py
```

The application will open in your browser at `http://localhost:8501`

## 📚 Usage Guide

### Step 1: Upload Your Content
Choose one of three input methods:
- **Local Video Upload:** Upload a video file from your computer
- **YouTube Link:** Provide a YouTube video URL
- **Script/Document Upload:** Upload a movie script or document

### Step 2: Generate AI Script
- The system will extract audio (if video) and transcribe it using Whisper
- AI will generate a Burmese movie recap script using Gemini
- You can edit the script before proceeding

### Step 3: Create Voiceover
- Select voice (Male/Female)
- Choose language (Burmese, English, Thai, etc.)
- Adjust voice speed and pitch
- Generate parallel voiceover for faster processing

### Step 4: Assemble Video
- Combine voiceover with original video
- Add custom logo/watermark
- Add Burmese subtitles
- Select output aspect ratio

### Step 5: Download
- Download your final recap video in MP4 format

## 🛠 Technology Stack

- **Frontend:** Streamlit
- **AI Models:**
  - Google Gemini 2.0 Flash (Script Generation)
  - OpenAI Whisper (Audio Transcription)
  - Edge TTS (Text-to-Speech)
- **Video Processing:** MoviePy, FFmpeg
- **Document Processing:** PyPDF2, python-docx
- **Video Downloading:** yt-dlp

## 📝 Roadmap

- [x] Phase 1: Core Setup & Input Handling
- [ ] Phase 2: AI Script Generation & Editing
- [ ] Phase 3: Audio & Voiceover Production
- [ ] Phase 4: Video Assembly & Branding
- [ ] Phase 5: Deployment & Project Management

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For issues, questions, or suggestions, please open an issue on GitHub.

## 🙏 Acknowledgments

This project is built upon the excellent work of various open-source projects:
- [Streamlit](https://streamlit.io/)
- [MoviePy](https://zulko.github.io/moviepy/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [Google Generative AI](https://ai.google.dev/)
- [OpenAI](https://openai.com/)

---

**Made with ❤️ for the Burmese community**

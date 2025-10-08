# 🎬 Memora AI Instagram Reel Generator

## 🧠 Overview

Memora is an advanced AI-powered **Streamlit** application that transforms static images into dynamic Instagram reels with AI narration.
The system integrates BERT5, Gemini 2.5 Flash, and a Retrieval-Augmented Generation (RAG) Database to intelligently generate emotional, context-driven video stories — complete with visuals, transitions, background music, and AI narration.

## 🚀 Workflow

1. **📸 Photo Upload** → User uploads multiple images
2. **🤖 BERT5 Analysis** → Extracts sentiment, mood, and contextual meaning from all images together
3. **🧠 RAG Database** → Matches extracted context to the most suitable specialized prompt
4. **✨ Gemini 2.5 Flash** → Generates video script and narration based on analysis
5. **🎤 AI Narration** → Creates voice-over using Hugging Face TTS models
6. **🎞️ MoviePy** → Combines images, transitions, background music, and narration into final MP4

**➡️ Final Output:** A complete Instagram reel with AI narration ready for download.

## ⚙️ Features

- **🧩 AI-Powered Context Extraction**: Uses BERT5 to understand emotion, tone, and meaning from multiple images together
- **🧠 Intelligent RAG Matching**: Dynamically selects prompts that align with detected sentiment and visual content
- **🎨 Gemini 2.5 Flash Integration**: Generates video scripts and narration based on image analysis
- **🎤 AI Narration**: Creates realistic voice-over using Hugging Face SpeechT5 TTS models
- **🎬 Automatic Video Composition**: Uses MoviePy to combine images, transitions, music, and narration
- **🌐 Streamlit Web Interface**: Clean, modern interface for easy image upload and video generation
- **🎵 Background Music**: Multiple music styles with automatic audio mixing
- **📱 Instagram-Ready**: Optimized for social media with proper aspect ratios and durations

## 🏗️ Project Structure
```
memora/
│
├── app.py                    # Streamlit main application
├── config.py                 # API key configuration
├── sentiment_analyzer.py      # BERT5 sentiment analysis
├── rag_database.py           # RAG database for prompt matching
├── video_generator.py        # Gemini + MoviePy video creation
├── ai_narrator.py            # AI narration with TTS
├── requirements.txt           # Python dependencies
│
├── assets/
│   └── music/                # Background music files
├── .env.example              # Environment variables template
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

⚙️ Setup Instructions

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/memora.git
   cd memora
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your Gemini API key
   # Get your API key from: https://aistudio.google.com/
   GEMINI_API_KEY=your_actual_api_key_here
   ```

4. Run the application
   ```bash
   streamlit run app.py
   ```

   App will run on 👉 http://localhost:8501

⚠️ **Important:** Never commit your `.env` file to version control!

## 🧠 Tech Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | Streamlit, HTML, CSS |
| **Backend** | Python |
| **AI Models** | BERT5 (sentiment analysis), Gemini 2.5 Flash (script generation) |
| **TTS** | Hugging Face SpeechT5 |
| **Retrieval System** | RAG with ChromaDB |
| **Video Rendering** | MoviePy |
| **Audio Processing** | FFmpeg, SoundFile |

## 📦 Output

Generated Instagram reels are automatically downloaded as MP4 files with:
- **AI-generated narration**
- **Background music**
- **Smooth transitions**
- **Instagram-optimized format**

## 🔐 Security

- ✅ No hardcoded API keys
- ✅ Environment variable configuration
- ✅ Secure `.gitignore` setup
- ✅ Clear setup instructions for users

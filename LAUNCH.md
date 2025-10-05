# 🎬 Memora - Launch Guide

## Quick Start

1. **Install Dependencies** (if not already done):
```bash
pip install -r requirements.txt
```

2. **Launch the Application**:
```bash
streamlit run app.py
```

3. **Access the App**: Open your browser to `http://localhost:8501`

## Features Implemented

✅ **AI Sentiment Analysis**: BERT5-based sentiment analysis for uploaded images
✅ **RAG Database**: Intelligent prompt matching system with ChromaDB
✅ **Gemini Integration**: Gemini 2.5 Flash Image API for creative video scripting
✅ **MoviePy Video Creation**: Professional video editing with background music
✅ **Modern UI**: High-quality 2025 Streamlit interface with gradient designs

## How to Use

1. **Upload Photos**: Select multiple images from your device
2. **AI Analysis**: The system automatically analyzes sentiment and context
3. **Prompt Matching**: RAG database finds the best video generation prompts
4. **Video Creation**: Gemini generates scripts, MoviePy creates the reel
5. **Download**: Get your Instagram-ready video file

## Test Images

The application works with any images, but you can test with:
- Bright, colorful images → Positive sentiment → Energetic reels
- Dark, moody images → Negative sentiment → Cinematic reels  
- Balanced images → Neutral sentiment → Professional reels

## API Configuration

- **Gemini API Key**: Already configured in `config.py`
- **Music Assets**: Place background music files in `assets/music/` directory

## Troubleshooting

- If you encounter import errors, run: `python test_app.py`
- For demo testing, run: `python demo.py`
- Check the console for any error messages

## Next Steps

1. Add your own background music files to `assets/music/`
2. Upload your photos and create amazing reels!
3. Customize the prompts in `rag_database.py` for your specific needs

---

**🎬 Ready to create amazing Instagram reels with AI!**


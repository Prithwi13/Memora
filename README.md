# 🎬 Memora - AI Photo to Reel Generator

Transform your photos into stunning Instagram reels using AI-powered sentiment analysis and video generation.

## Features

- **AI Sentiment Analysis**: Uses BERT5 model to analyze photo sentiment and context
- **RAG Database**: Intelligent prompt matching for optimal video generation
- **Gemini Integration**: Leverages Gemini 2.5 Flash Image for creative video scripting
- **MoviePy Video Creation**: Professional video editing with background music
- **Modern UI**: High-quality 2025 Streamlit interface

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
# Create .env file with your Gemini API key
GEMINI_API_KEY=your_api_key_here
```

3. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Upload your photos
2. AI analyzes sentiment and context
3. RAG database matches optimal prompts
4. Gemini generates video script
5. MoviePy creates your Instagram reel
6. Download and share!

## API Keys

- **Gemini API**: Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## Music Assets

Place your background music files in `assets/music/`:
- `upbeat_electronic.mp3`
- `chill_ambient.mp3`
- `happy_pop.mp3`
- `romantic_piano.mp3`
- `adventure_cinematic.mp3`

## Tech Stack

- **Frontend**: Streamlit
- **AI Models**: BERT5, Gemini 2.5 Flash
- **Video Processing**: MoviePy
- **Database**: ChromaDB
- **Embeddings**: Sentence Transformers


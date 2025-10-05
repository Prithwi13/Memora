🎬 HackUTA AI Cinematic Generator
🧠 Overview

HackUTA AI Cinematic Generator is an advanced AI-powered Flask application that transforms static images into dynamic cinematic videos.
The system integrates BERT5, Gemini 2.5 Flash, and a Retrieval-Augmented Generation (RAG) Database to intelligently generate emotional, context-driven video stories — complete with visuals, transitions, and background audio.

🚀 Workflow
📸 Photo Upload
↓
🤖 BERT5 Model
→ Extracts sentiment, mood, and contextual meaning from uploaded images
↓
🧠 RAG Database
→ Matches extracted context to the most suitable specialized prompt
↓
✨ Gemini 2.5 Flash (Image Generation)
→ Generates stylized cinematic frames from refined prompts and images
↓
🎞️ MoviePy
→ Combines all generated frames, transitions, and audio into a final MP4 video

➡️ Final Output: A complete cinematic video stored in the outputs/ folder.

⚙️ Features

🧩 AI-Powered Context Extraction: Uses BERT5 to understand emotion, tone, and meaning from multiple images together.

🧠 Intelligent RAG Matching: Dynamically selects prompts that align with detected sentiment and visual content.

🎨 Gemini 2.5 Flash Integration: Produces artistic, frame-level cinematic imagery guided by the selected prompt.

🎬 Automatic Video Composition: Uses MoviePy to combine generated visuals and sound into a cohesive short film.

🌐 Web Interface via Flask: Intuitive interface to upload images and preview generated results locally.

🏗️ Project Structure
hackuta-main/
│
├── app.py # Flask main application
├── config.py # Config settings for API and model paths
├── rag*database.json # RAG database with specialized prompts
├── requirements.txt # Python dependencies
│
├── templates/ # Frontend HTML templates
├── static/ # Static assets (CSS, JS, etc.)
├── uploads/ # Temporary image uploads
├── outputs/ # Generated MP4 video outputs
│
├── services/ # Internal services for AI processing
└── test*\*.py # Test scripts for components

⚙️ Setup Instructions

1. Clone the repository
   git clone https://github.com/yourusername/hackuta-main.git
   cd hackuta-main

2. Install dependencies

Make sure Python 3.9+ is installed:

pip install -r requirements.txt

3. Run the application
   python3 app.py

App will run on
👉 http://localhost:5003

🧠 Tech Stack
Component Technology
Frontend Flask, HTML, CSS, JavaScript
Backend Python
AI Models BERT5 (sentiment/context extraction)
Retrieval System RAG (specialized cinematic prompts)
Image Generation Gemini 2.5 Flash
Video Rendering MoviePy
Storage Local filesystem (uploads/outputs)
📦 Output

Generated cinematic videos are saved in:

outputs/

Each file is named automatically (e.g., generated_video_001.mp4).

#!/usr/bin/env python3
"""
Memora Application Launcher
"""

import subprocess
import sys
import os

def main():
    """Launch the Memora application"""
    print("🎬 Starting Memora - AI Photo to Reel Generator")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("app.py"):
        print("❌ Error: app.py not found. Please run this script from the Memora directory.")
        sys.exit(1)
    
    # Check if requirements are installed
    try:
        import streamlit
        import torch
        import transformers
        import google.generativeai
        import moviepy
        import chromadb
        from sentence_transformers import SentenceTransformer
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install requirements first:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    print("✅ All dependencies found")
    print("🚀 Launching Streamlit application...")
    print("\nThe application will open in your browser at: http://localhost:8501")
    print("Press Ctrl+C to stop the application")
    print("=" * 50)
    
    # Launch Streamlit
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()


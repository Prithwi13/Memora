#!/usr/bin/env python3
"""
Test script to verify Memora application components
"""

import sys
import os

def test_imports():
    """Test if all required packages can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import torch
        print("✅ PyTorch imported successfully")
    except ImportError as e:
        print(f"❌ PyTorch import failed: {e}")
        return False
    
    try:
        import transformers
        print("✅ Transformers imported successfully")
    except ImportError as e:
        print(f"❌ Transformers import failed: {e}")
        return False
    
    try:
        import google.generativeai as genai
        print("✅ Google Generative AI imported successfully")
    except ImportError as e:
        print(f"❌ Google Generative AI import failed: {e}")
        return False
    
    try:
        import moviepy.editor as mp
        print("✅ MoviePy imported successfully")
    except ImportError as e:
        print(f"❌ MoviePy import failed: {e}")
        return False
    
    try:
        import chromadb
        print("✅ ChromaDB imported successfully")
    except ImportError as e:
        print(f"❌ ChromaDB import failed: {e}")
        return False
    
    try:
        from sentence_transformers import SentenceTransformer
        print("✅ Sentence Transformers imported successfully")
    except ImportError as e:
        print(f"❌ Sentence Transformers import failed: {e}")
        return False
    
    return True

def test_config():
    """Test configuration"""
    print("\n🔧 Testing configuration...")
    
    try:
        from config import GEMINI_API_KEY
        if GEMINI_API_KEY:
            print("✅ Gemini API key configured")
        else:
            print("⚠️ Gemini API key not set")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_components():
    """Test application components"""
    print("\n🧩 Testing components...")
    
    try:
        from sentiment_analyzer import SentimentAnalyzer
        analyzer = SentimentAnalyzer()
        print("✅ Sentiment Analyzer initialized")
    except Exception as e:
        print(f"❌ Sentiment Analyzer failed: {e}")
        return False
    
    try:
        from rag_database import RAGDatabase
        rag = RAGDatabase()
        print("✅ RAG Database initialized")
    except Exception as e:
        print(f"❌ RAG Database failed: {e}")
        return False
    
    try:
        from video_generator import VideoGenerator
        generator = VideoGenerator()
        print("✅ Video Generator initialized")
    except Exception as e:
        print(f"❌ Video Generator failed: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🎬 Memora Application Test Suite")
    print("=" * 40)
    
    all_tests_passed = True
    
    # Test imports
    if not test_imports():
        all_tests_passed = False
    
    # Test configuration
    if not test_config():
        all_tests_passed = False
    
    # Test components
    if not test_components():
        all_tests_passed = False
    
    print("\n" + "=" * 40)
    if all_tests_passed:
        print("🎉 All tests passed! Application is ready to run.")
        print("\nTo start the application, run:")
        print("streamlit run app.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\nTo install missing dependencies, run:")
        print("pip install -r requirements.txt")
    
    return all_tests_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)


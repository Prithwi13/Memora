#!/usr/bin/env python3
"""
Demo script to test Memora with sample images
"""

import os
import sys
from PIL import Image
import numpy as np
import tempfile

def create_sample_images():
    """Create sample images for testing"""
    sample_images = []
    
    # Create a bright, colorful image (Positive sentiment)
    bright_image = Image.new('RGB', (400, 400), color=(255, 200, 100))
    sample_images.append(('bright_colorful.jpg', bright_image, 'Positive'))
    
    # Create a dark, moody image (Negative sentiment)
    dark_image = Image.new('RGB', (400, 400), color=(50, 50, 100))
    sample_images.append(('dark_moody.jpg', dark_image, 'Negative'))
    
    # Create a neutral image
    neutral_image = Image.new('RGB', (400, 400), color=(128, 128, 128))
    sample_images.append(('neutral_gray.jpg', neutral_image, 'Neutral'))
    
    return sample_images

def test_sentiment_analysis():
    """Test sentiment analysis with sample images"""
    print("🧪 Testing Sentiment Analysis...")
    
    try:
        from sentiment_analyzer import SentimentAnalyzer
        analyzer = SentimentAnalyzer()
        
        sample_images = create_sample_images()
        
        for filename, image, expected_sentiment in sample_images:
            sentiment, context = analyzer.analyze_image(image)
            print(f"📸 {filename}: {sentiment} - {context}")
            
            # Save sample image for testing
            image.save(f"sample_{filename}")
        
        print("✅ Sentiment analysis test completed")
        return True
        
    except Exception as e:
        print(f"❌ Sentiment analysis test failed: {e}")
        return False

def test_rag_database():
    """Test RAG database functionality"""
    print("\n🧪 Testing RAG Database...")
    
    try:
        from rag_database import RAGDatabase
        rag = RAGDatabase()
        
        # Test prompt matching
        test_cases = [
            ("Positive", "bright and colorful scene with vibrant colors"),
            ("Negative", "dark and moody scene with dramatic lighting"),
            ("Neutral", "balanced scene with natural lighting and colors")
        ]
        
        for sentiment, context in test_cases:
            prompt = rag.get_matching_prompt(sentiment, context)
            print(f"🎯 {sentiment} + {context[:30]}... -> {prompt[:50]}...")
        
        print("✅ RAG database test completed")
        return True
        
    except Exception as e:
        print(f"❌ RAG database test failed: {e}")
        return False

def test_video_generation():
    """Test video generation (without actually creating video files)"""
    print("\n🧪 Testing Video Generation Setup...")
    
    try:
        from video_generator import VideoGenerator
        generator = VideoGenerator()
        
        # Test Gemini API connection
        print("🔗 Testing Gemini API connection...")
        test_script = generator._generate_video_script([], "Modern", 30)
        print(f"📝 Generated script preview: {test_script[:100]}...")
        
        print("✅ Video generation test completed")
        return True
        
    except Exception as e:
        print(f"❌ Video generation test failed: {e}")
        return False

def main():
    """Run all demo tests"""
    print("🎬 Memora Demo Test Suite")
    print("=" * 40)
    
    all_tests_passed = True
    
    # Test sentiment analysis
    if not test_sentiment_analysis():
        all_tests_passed = False
    
    # Test RAG database
    if not test_rag_database():
        all_tests_passed = False
    
    # Test video generation
    if not test_video_generation():
        all_tests_passed = False
    
    print("\n" + "=" * 40)
    if all_tests_passed:
        print("🎉 All demo tests passed!")
        print("\n🚀 Ready to launch the application:")
        print("streamlit run app.py")
    else:
        print("❌ Some demo tests failed.")
    
    return all_tests_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)



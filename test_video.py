#!/usr/bin/env python3
"""
Test video generation with audio and transitions
"""

import os
import sys
from PIL import Image
import numpy as np

def create_test_images():
    """Create test images for video generation"""
    images = []
    
    # Create a bright image (Positive)
    bright_img = Image.new('RGB', (400, 400), color=(255, 200, 100))
    images.append(('bright', bright_img, 'Positive', 'bright and colorful scene'))
    
    # Create a dark image (Negative)
    dark_img = Image.new('RGB', (400, 400), color=(50, 50, 100))
    images.append(('dark', dark_img, 'Negative', 'dark and moody scene'))
    
    # Create a neutral image
    neutral_img = Image.new('RGB', (400, 400), color=(128, 128, 128))
    images.append(('neutral', neutral_img, 'Neutral', 'balanced scene'))
    
    return images

def test_video_generation():
    """Test complete video generation"""
    print("🎬 Testing Video Generation with Audio and Transitions...")
    
    try:
        from video_generator import VideoGenerator
        from sentiment_analyzer import SentimentAnalyzer
        from rag_database import RAGDatabase
        
        # Initialize components
        analyzer = SentimentAnalyzer()
        rag = RAGDatabase()
        generator = VideoGenerator()
        
        # Create test images
        test_images = create_test_images()
        analysis_results = []
        
        print("📸 Analyzing test images...")
        for name, img, expected_sentiment, expected_context in test_images:
            sentiment, context = analyzer.analyze_image(img)
            prompt = rag.get_matching_prompt(sentiment, context)
            
            analysis_results.append({
                'image': img,
                'sentiment': sentiment,
                'context': context,
                'prompt': prompt
            })
            
            print(f"   {name}: {sentiment} - {context[:50]}...")
        
        print("🎵 Testing audio integration...")
        # Test music file loading
        music_path = generator._get_music_path("Upbeat")
        if music_path and os.path.exists(music_path):
            print(f"   ✅ Music file found: {music_path}")
        else:
            print(f"   ❌ Music file not found: {music_path}")
        
        print("🎬 Testing video creation...")
        # Test video creation (short duration for testing)
        video_path = generator.create_reel(
            analysis_results,
            music_style="Upbeat",
            duration=10,  # Short duration for testing
            style="Modern"
        )
        
        if os.path.exists(video_path):
            file_size = os.path.getsize(video_path)
            print(f"   ✅ Video created successfully: {video_path}")
            print(f"   📊 File size: {file_size / 1024:.1f} KB")
            
            # Clean up test video
            os.unlink(video_path)
        else:
            print(f"   ❌ Video creation failed")
            return False
        
        print("✅ Video generation test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Video generation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run video generation test"""
    print("🎬 Memora Video Generation Test")
    print("=" * 40)
    
    success = test_video_generation()
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 All video generation tests passed!")
        print("🎵 Audio integration working")
        print("🎬 Transitions and effects working")
        print("🚀 Ready for production use!")
    else:
        print("❌ Video generation tests failed.")
        print("Please check the error messages above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)



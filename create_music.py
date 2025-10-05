#!/usr/bin/env python3
"""
Create sample music files for testing
"""

import numpy as np
import wave
import os

def create_simple_tone(frequency, duration, sample_rate=44100):
    """Create a simple tone"""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave_data = np.sin(2 * np.pi * frequency * t)
    return (wave_data * 32767).astype(np.int16)

def create_music_file(filename, base_frequency, duration=30):
    """Create a simple music file"""
    sample_rate = 44100
    music_data = np.zeros(int(sample_rate * duration))
    
    # Create a simple melody with the base frequency
    for i in range(8):  # 8 notes
        start_time = i * (duration / 8)
        end_time = (i + 1) * (duration / 8)
        start_sample = int(start_time * sample_rate)
        end_sample = int(end_time * sample_rate)
        
        # Vary the frequency slightly for melody
        freq = base_frequency * (1 + i * 0.1)
        tone = create_simple_tone(freq, end_time - start_time, sample_rate)
        
        # Add fade in/out
        fade_samples = int(0.05 * sample_rate)  # 0.05 second fade
        if len(tone) > 2 * fade_samples:
            fade_in = np.linspace(0, 1, fade_samples).astype(np.float32)
            fade_out = np.linspace(1, 0, fade_samples).astype(np.float32)
            tone[:fade_samples] = (tone[:fade_samples].astype(np.float32) * fade_in).astype(np.int16)
            tone[-fade_samples:] = (tone[-fade_samples:].astype(np.float32) * fade_out).astype(np.int16)
        
        music_data[start_sample:end_sample] = tone * 0.3
    
    # Save as WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(music_data.tobytes())

def create_all_music_files():
    """Create all sample music files"""
    music_dir = "assets/music"
    os.makedirs(music_dir, exist_ok=True)
    
    # Upbeat Electronic (higher frequency)
    create_music_file(f"{music_dir}/upbeat_electronic.wav", 440, 30)
    
    # Chill Ambient (lower frequency)
    create_music_file(f"{music_dir}/chill_ambient.wav", 220, 30)
    
    # Happy Pop (medium-high frequency)
    create_music_file(f"{music_dir}/happy_pop.wav", 523, 30)
    
    # Romantic Piano (medium frequency)
    create_music_file(f"{music_dir}/romantic_piano.wav", 330, 30)
    
    # Adventure Cinematic (low frequency)
    create_music_file(f"{music_dir}/adventure_cinematic.wav", 110, 30)
    
    print("✅ Created sample music files:")
    for filename in os.listdir(music_dir):
        print(f"   🎵 {filename}")

if __name__ == "__main__":
    create_all_music_files()
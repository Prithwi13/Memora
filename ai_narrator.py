#!/usr/bin/env python3
"""
AI Narrator using Hugging Face TTS models
"""

import torch
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
import soundfile as sf
import tempfile
import os
import numpy as np

# Try to import streamlit, but don't fail if it's not available
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False
    # Create a mock st object for non-streamlit environments
    class MockSt:
        def info(self, msg): print(f"INFO: {msg}")
        def success(self, msg): print(f"SUCCESS: {msg}")
        def warning(self, msg): print(f"WARNING: {msg}")
        def error(self, msg): print(f"ERROR: {msg}")
    st = MockSt()

class AINarrator:
    def __init__(self):
        """Initialize AI narrator with TTS models"""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.load_models()
    
    def load_models(self):
        """Load TTS models"""
        try:
            st.info("🎤 Loading AI narrator models...")
            
            # Load SpeechT5 models
            self.processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
            self.model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
            self.vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
            
            # Move to device
            self.model.to(self.device)
            self.vocoder.to(self.device)
            
            st.success("✅ AI narrator models loaded successfully!")
            
        except Exception as e:
            st.warning(f"⚠️ Could not load TTS models: {e}")
            st.info("🔄 Using fallback text-to-speech...")
            self.model = None
            self.processor = None
            self.vocoder = None
    
    def generate_narration(self, script, sentiment="Neutral"):
        """
        Generate AI narration from script
        
        Args:
            script: Video script text
            sentiment: Overall sentiment (Positive, Negative, Neutral)
        
        Returns:
            Path to generated audio file
        """
        try:
            if self.model is None:
                return self._fallback_tts(script, sentiment)
            
            st.info("🎙️ Generating AI narration...")
            
            # Extract key sentences from script
            narration_text = self._extract_narration_text(script, sentiment)
            
            # Generate speech
            inputs = self.processor(text=narration_text, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate speech
            with torch.no_grad():
                # Keep input_ids as Long (integer) for embedding, but ensure attention_mask is proper type
                input_ids = inputs["input_ids"].long()  # Keep as Long for embedding
                attention_mask = inputs["attention_mask"].long()  # Keep as Long for attention
                
                speech = self.model.generate_speech(
                    input_ids, 
                    attention_mask
                )
                # Ensure speech tensor is float before vocoder
                speech = speech.float() if speech.dtype != torch.float32 else speech
                audio = self.vocoder(speech)
            
            # Convert to numpy and save
            audio_np = audio.cpu().numpy()
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
                sf.write(tmp.name, audio_np, 22050)
                audio_path = tmp.name
            
            st.success("✅ AI narration generated successfully!")
            return audio_path
            
        except Exception as e:
            st.warning(f"⚠️ AI narration failed: {e}")
            return self._fallback_tts(script, sentiment)
    
    def _extract_narration_text(self, script, sentiment):
        """Extract key narration text from script"""
        # Simple extraction - in practice, you'd use more sophisticated NLP
        lines = script.split('\n')
        key_lines = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['scene', 'moment', 'capture', 'experience', 'journey']):
                key_lines.append(line.strip())
        
        if not key_lines:
            # Fallback narration based on sentiment
            if sentiment == "Positive":
                return "Welcome to this amazing journey! Let's explore these beautiful moments together."
            elif sentiment == "Negative":
                return "Join us as we dive into these powerful and dramatic scenes."
            else:
                return "Discover the story behind these carefully captured moments."
        
        return " ".join(key_lines[:3])  # Use first 3 key lines
    
    def _fallback_tts(self, script, sentiment):
        """Fallback TTS using system TTS"""
        try:
            st.info("🔄 Using system text-to-speech...")
            
            # Extract narration text
            narration_text = self._extract_narration_text(script, sentiment)
            
            # Use system TTS (macOS)
            import subprocess
            
            with tempfile.NamedTemporaryFile(suffix='.aiff', delete=False) as tmp:
                # Use macOS say command
                subprocess.run([
                    'say', '-v', 'Alex', '-o', tmp.name, narration_text
                ], check=True)
                
                # Convert to WAV
                audio_path = tmp.name.replace('.aiff', '.wav')
                subprocess.run([
                    'ffmpeg', '-i', tmp.name, '-acodec', 'pcm_s16le', 
                    '-ar', '22050', audio_path, '-y'
                ], check=True)
                
                os.unlink(tmp.name)
                return audio_path
                
        except Exception as e:
            st.warning(f"⚠️ Fallback TTS failed: {e}")
            return None
    
    def get_narration_style(self, sentiment):
        """Get narration style based on sentiment"""
        styles = {
            "Positive": {
                "tone": "energetic and upbeat",
                "pace": "moderate to fast",
                "emotion": "excited and joyful"
            },
            "Negative": {
                "tone": "dramatic and intense", 
                "pace": "slow and deliberate",
                "emotion": "powerful and emotional"
            },
            "Neutral": {
                "tone": "professional and clear",
                "pace": "steady and calm",
                "emotion": "balanced and informative"
            }
        }
        return styles.get(sentiment, styles["Neutral"])

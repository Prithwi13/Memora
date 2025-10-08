import google.generativeai as genai
import moviepy.editor as mp
from moviepy.video.fx import resize, fadeout, fadein
from PIL import Image
import tempfile
import os
import streamlit as st
import numpy as np
from config import GEMINI_API_KEY
from ai_narrator import AINarrator

class VideoGenerator:
    def __init__(self):
        """Initialize the video generator with Gemini API"""
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.narrator = AINarrator()
    
    def create_reel(self, analysis_results, music_style="Upbeat", duration=30, style="Modern"):
        """
        Create an Instagram reel from analyzed images
        
        Args:
            analysis_results: List of analysis results with images, sentiment, context, and prompts
            music_style: Style of background music
            duration: Duration of the video in seconds
            style: Visual style of the video
        
        Returns:
            Path to the generated video file
        """
        try:
            st.info("🎬 Starting video generation process...")
            
            # Generate video script using Gemini
            st.info("🤖 Step 1: Generating video script with Gemini AI...")
            script = self._generate_video_script(analysis_results, style, duration)
            
            # Create video clips from images
            st.info("🎞️ Step 2: Creating video clips from images...")
            clips = self._create_video_clips(analysis_results, script, duration)
            
            # Generate AI narration
            st.info("🎤 Step 3: Generating AI narration...")
            narration_path = self.narrator.generate_narration(script, analysis_results[0]['sentiment'])
            
            # Add background music and narration
            st.info("🎵 Step 4: Adding background music and narration...")
            final_video = self._add_background_music(clips, music_style, duration, narration_path)
            
            # Save video
            st.info("💾 Step 5: Saving final video...")
            output_path = self._save_video(final_video)
            
            st.success("🎉 Video generation completed successfully!")
            return output_path
            
        except Exception as e:
            st.error(f"Error creating video: {e}")
            raise
    
    def _generate_video_script(self, analysis_results, style, duration):
        """Generate video script using Gemini AI"""
        try:
            st.info("🤖 Calling Gemini AI to generate video script...")
            
            # Prepare context for Gemini
            context = f"""
            Create a video script for an Instagram reel with the following specifications:
            - Style: {style}
            - Duration: {duration} seconds
            - Number of images: {len(analysis_results)}
            
            Image analysis:
            """
            
            for i, result in enumerate(analysis_results):
                context += f"""
                Image {i+1}:
                - Sentiment: {result['sentiment']}
                - Context: {result['context']}
                - AI Prompt: {result['prompt']}
                """
            
            context += """
            
            Generate a detailed video script that includes:
            1. Timing for each image (in seconds)
            2. Transition effects between images
            3. Camera movements (zoom, pan, etc.)
            4. Color grading suggestions
            5. Text overlays or captions
            6. Overall pacing and rhythm
            
            Format the response as a structured script with clear timing and effects.
            """
            
            # Generate script using Gemini
            st.info("📡 Sending request to Gemini API...")
            response = self.model.generate_content(context)
            script = response.text
            
            st.success("✅ Gemini AI script generated successfully!")
            st.info(f"📝 Generated script preview: {script[:200]}...")
            
            return script
            
        except Exception as e:
            st.error(f"❌ Gemini script generation failed: {e}")
            st.warning("🔄 Using fallback script...")
            # Fallback to basic script
            return self._create_fallback_script(analysis_results, duration)
    
    def _create_fallback_script(self, analysis_results, duration):
        """Create a basic fallback script"""
        clip_duration = duration / len(analysis_results)
        
        script = {
            "clips": [],
            "transitions": [],
            "effects": []
        }
        
        for i, result in enumerate(analysis_results):
            script["clips"].append({
                "image_index": i,
                "duration": clip_duration,
                "effect": "zoom_in" if result['sentiment'] == 'Positive' else "fade_in",
                "transition": "crossfade" if i < len(analysis_results) - 1 else "fade_out"
            })
        
        return script
    
    def _create_video_clips(self, analysis_results, script, duration):
        """Create video clips from images with transitions and effects"""
        clips = []
        
        try:
            clip_duration = duration / len(analysis_results)
            
            for i, result in enumerate(analysis_results):
                # Create temporary file for image
                with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
                    result['image'].save(tmp.name, 'JPEG')
                    image_path = tmp.name
                
                # Create video clip from image
                clip = mp.ImageClip(image_path, duration=clip_duration)
                
                # Resize to Instagram standard (9:16 aspect ratio)
                clip = clip.resize(height=1080)
                
                # Apply modern 2025 Instagram reel effects
                if result['sentiment'] == 'Positive':
                    # Ken Burns effect with smooth pan and zoom
                    clip = clip.resize(lambda t: 1 + 0.15 * np.sin(t * np.pi / clip_duration))
                    # Add vibrant color grading
                    clip = clip.fx(mp.vfx.colorx, 1.2)
                    # Add subtle glow effect
                    clip = clip.fx(mp.vfx.lum_contrast, 1.1, 1.05)
                elif result['sentiment'] == 'Negative':
                    # Cinematic slow zoom with dramatic lighting
                    clip = clip.resize(lambda t: 1 + 0.1 * t / clip_duration)
                    # Add moody color grading
                    clip = clip.fx(mp.vfx.colorx, 0.8)
                    clip = clip.fx(mp.vfx.lum_contrast, 0.9, 1.2)
                else:
                    # Smooth parallax effect
                    clip = clip.resize(lambda t: 1 + 0.08 * np.sin(t * 2 * np.pi / clip_duration))
                    # Add clean, modern color grading
                    clip = clip.fx(mp.vfx.colorx, 1.05)
                
                # Add modern fade effects
                if i == 0:
                    clip = clip.fadein(0.5)  # Quick fade in
                if i == len(analysis_results) - 1:
                    clip = clip.fadeout(0.5)  # Quick fade out
                
                # Add smooth crossfade transitions between clips
                if i > 0:
                    clip = clip.fadein(0.2)  # Subtle crossfade
                
                clips.append(clip)
                
                # Clean up temporary file
                os.unlink(image_path)
        
        except Exception as e:
            st.warning(f"Error creating clips: {e}")
            # Create simple clips as fallback
            clips = self._create_simple_clips(analysis_results, duration)
        
        # Ensure we have at least one clip
        if not clips:
            st.error("Failed to create any video clips. Please try with different images.")
            return []
        
        return clips
    
    def _create_simple_clips(self, analysis_results, duration):
        """Create simple video clips as fallback"""
        clips = []
        clip_duration = duration / len(analysis_results)
        
        for result in analysis_results:
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
                result['image'].save(tmp.name, 'JPEG')
                
                clip = mp.ImageClip(tmp.name, duration=clip_duration)
                clip = clip.resize(height=1080)  # Instagram standard
                clips.append(clip)
                
                os.unlink(tmp.name)
        
        return clips
    
    def _add_background_music(self, clips, music_style, duration, narration_path=None):
        """Add background music and narration to the video"""
        try:
            # Check if clips list is empty
            if not clips:
                st.error("No video clips were created. Please check your images.")
                return None
            
            # Concatenate video clips with smooth transitions
            if len(clips) == 1:
                final_video = clips[0]
            else:
                # Use compose method with shorter transition for modern look
                final_video = mp.concatenate_videoclips(clips, method="compose", transition=0.3)
            
            # Get the actual video duration - ensure it's a proper float
            try:
                video_duration = float(final_video.duration)
                if video_duration <= 0:
                    st.warning("Video duration is invalid, using default")
                    video_duration = 30.0
            except (AttributeError, TypeError, ValueError) as e:
                st.warning(f"Could not get video duration: {e}, using default")
                video_duration = 30.0
            
            # Get music path
            music_path = self._get_music_path(music_style)
            
            if music_path and os.path.exists(music_path):
                try:
                    # Load audio with proper error handling
                    audio = mp.AudioFileClip(music_path)
                    
                    # Validate audio object
                    if not hasattr(audio, 'duration'):
                        st.warning("Audio file loaded but has no duration attribute")
                        audio = mp.AudioClip(lambda t: 0, duration=video_duration)
                    elif audio.duration is None or audio.duration <= 0:
                        st.warning("Audio file has invalid duration")
                        audio = mp.AudioClip(lambda t: 0, duration=video_duration)
                    else:
                        # Adjust audio duration to match video
                        if audio.duration > video_duration:
                            audio = audio.subclip(0, video_duration)
                        elif audio.duration < video_duration:
                            # Loop audio if it's shorter than video
                            loops_needed = int(video_duration / audio.duration) + 1
                            audio = mp.concatenate_audioclips([audio] * loops_needed).subclip(0, video_duration)
                    
                    # Set audio volume (reduce to 30% to leave room for narration)
                    audio = audio.volumex(0.3)
                    
                    # Add narration if available
                    if narration_path and os.path.exists(narration_path):
                        try:
                            st.info("🎤 Adding AI narration...")
                            narration = mp.AudioFileClip(narration_path)
                            
                            # Adjust narration volume and duration
                            narration = narration.volumex(0.8)  # Louder than music
                            if narration.duration > video_duration:
                                narration = narration.subclip(0, video_duration)
                            
                            # Mix narration with background music
                            mixed_audio = mp.CompositeAudioClip([audio, narration])
                            final_video = final_video.set_audio(mixed_audio)
                            
                            st.success("🎤 Added AI narration with background music")
                            
                        except Exception as narration_error:
                            st.warning(f"Narration error: {narration_error}")
                            # Use just background music
                            final_video = final_video.set_audio(audio)
                            st.success(f"🎵 Added {music_style} background music")
                    else:
                        # Add just background music
                        final_video = final_video.set_audio(audio)
                        st.success(f"🎵 Added {music_style} background music")
                    
                except Exception as audio_error:
                    st.warning(f"Audio loading error: {audio_error}")
                    # Create silent audio track
                    try:
                        silent_audio = mp.AudioClip(lambda t: 0, duration=video_duration)
                        final_video = final_video.set_audio(silent_audio)
                    except Exception as silent_error:
                        st.warning(f"Could not create silent audio: {silent_error}")
                        # Return video without audio
                        pass
            else:
                st.warning(f"Music file not found: {music_path}")
                # Create silent audio track
                try:
                    silent_audio = mp.AudioClip(lambda t: 0, duration=video_duration)
                    final_video = final_video.set_audio(silent_audio)
                except Exception as silent_error:
                    st.warning(f"Could not create silent audio: {silent_error}")
                    # Return video without audio
                    pass
            
            return final_video
            
        except Exception as e:
            st.warning(f"Error adding music: {e}")
            # Return video without music
            if len(clips) == 1:
                return clips[0]
            else:
                return mp.concatenate_videoclips(clips, method="compose")
    
    def _get_music_path(self, music_style):
        """Get path to background music file"""
        music_files = {
            "Upbeat": "assets/music/upbeat_electronic.wav",
            "Chill": "assets/music/chill_ambient.wav",
            "Happy": "assets/music/happy_pop.wav",
            "Romantic": "assets/music/romantic_piano.wav",
            "Adventure": "assets/music/adventure_cinematic.wav"
        }
        
        return music_files.get(music_style, None)
    
    def _save_video(self, video_clip):
        """Save the final video to a temporary file"""
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp:
            output_path = tmp.name
        
        # Write video file
        video_clip.write_videofile(
            output_path,
            fps=24,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )
        
        # Close video clip to free memory
        video_clip.close()
        
        return output_path

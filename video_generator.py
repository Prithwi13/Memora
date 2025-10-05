import google.generativeai as genai
import moviepy.editor as mp
from moviepy.video.fx import resize, fadeout, fadein
from PIL import Image
import tempfile
import os
import streamlit as st
from config import GEMINI_API_KEY

class VideoGenerator:
    def __init__(self):
        """Initialize the video generator with Gemini API"""
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
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
            # Generate video script using Gemini
            script = self._generate_video_script(analysis_results, style, duration)
            
            # Create video clips from images
            clips = self._create_video_clips(analysis_results, script, duration)
            
            # Add background music
            final_video = self._add_background_music(clips, music_style, duration)
            
            # Save video
            output_path = self._save_video(final_video)
            
            return output_path
            
        except Exception as e:
            st.error(f"Error creating video: {e}")
            raise
    
    def _generate_video_script(self, analysis_results, style, duration):
        """Generate video script using Gemini AI"""
        try:
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
            response = self.model.generate_content(context)
            script = response.text
            
            return script
            
        except Exception as e:
            st.warning(f"Gemini script generation failed: {e}")
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
                
                # Apply enhanced effects based on sentiment for shorter duration
                if result['sentiment'] == 'Positive':
                    # Dynamic zoom with rotation for positive images
                    clip = clip.resize(lambda t: 1 + 0.3 * t / clip_duration)
                    clip = clip.rotate(lambda t: 2 * t / clip_duration)  # Subtle rotation
                    # Add brightness and saturation boost
                    clip = clip.fx(mp.vfx.colorx, 1.3)
                elif result['sentiment'] == 'Negative':
                    # Dramatic zoom with fade for negative images
                    clip = clip.resize(lambda t: 1 + 0.4 * t / clip_duration)
                    # Add dramatic contrast and darkening
                    clip = clip.fx(mp.vfx.colorx, 0.7)
                else:
                    # Smooth zoom with slight pan for neutral
                    clip = clip.resize(lambda t: 1 + 0.2 * t / clip_duration)
                    # Add subtle color enhancement
                    clip = clip.fx(mp.vfx.colorx, 1.1)
                
                # Add fade effects
                if i == 0:
                    clip = clip.fadein(0.8)
                if i == len(analysis_results) - 1:
                    clip = clip.fadeout(0.8)
                
                # Add crossfade transitions between clips
                if i > 0:
                    clip = clip.fadein(0.3)
                
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
    
    def _add_background_music(self, clips, music_style, duration):
        """Add background music to the video"""
        try:
            # Check if clips list is empty
            if not clips:
                st.error("No video clips were created. Please check your images.")
                return None
            
            # Concatenate video clips with crossfade transitions
            if len(clips) == 1:
                final_video = clips[0]
            else:
                final_video = mp.concatenate_videoclips(clips, method="compose", transition=0.5)
            
            # Get the actual video duration
            video_duration = final_video.duration
            
            # Get music path
            music_path = self._get_music_path(music_style)
            
            if music_path and os.path.exists(music_path):
                try:
                    # Load audio
                    audio = mp.AudioFileClip(music_path)
                    
                    # Adjust audio duration to match video
                    if audio.duration > video_duration:
                        audio = audio.subclip(0, video_duration)
                    elif audio.duration < video_duration:
                        # Loop audio if it's shorter than video
                        loops_needed = int(video_duration / audio.duration) + 1
                        audio = mp.concatenate_audioclips([audio] * loops_needed).subclip(0, video_duration)
                    
                    # Set audio volume (reduce to 40% to not overpower)
                    audio = audio.volumex(0.4)
                    
                    # Add audio to video
                    final_video = final_video.set_audio(audio)
                    
                    st.success(f"🎵 Added {music_style} background music")
                    
                except Exception as audio_error:
                    st.warning(f"Audio loading error: {audio_error}")
                    # Create silent audio track
                    silent_audio = mp.AudioClip(lambda t: 0, duration=video_duration)
                    final_video = final_video.set_audio(silent_audio)
            else:
                st.warning(f"Music file not found: {music_path}")
                # Create silent audio track
                silent_audio = mp.AudioClip(lambda t: 0, duration=video_duration)
                final_video = final_video.set_audio(silent_audio)
            
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

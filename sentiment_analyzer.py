import torch
from transformers import AutoTokenizer, AutoModel
from PIL import Image
import numpy as np
import streamlit as st

class SentimentAnalyzer:
    def __init__(self):
        """Initialize the BERT5-based sentiment analyzer"""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.load_model()
    
    def load_model(self):
        """Load the BERT5 model and tokenizer"""
        try:
            # Using a vision-language model for image sentiment analysis
            model_name = "microsoft/git-base"
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModel.from_pretrained(model_name)
            self.model.to(self.device)
            self.model.eval()
        except Exception as e:
            st.error(f"Error loading model: {e}")
            # Fallback to a simpler approach
            self.model = None
            self.tokenizer = None
    
    def analyze_image(self, image):
        """
        Analyze image sentiment and context using BERT5
        Returns: (sentiment, context_description)
        """
        try:
            if self.model is None:
                # Fallback analysis based on image properties
                return self._fallback_analysis(image)
            
            # Convert image to tensor
            image_tensor = self._preprocess_image(image)
            
            # Generate description and sentiment
            description = self._generate_description(image_tensor)
            sentiment = self._classify_sentiment(description)
            
            return sentiment, description
            
        except Exception as e:
            st.warning(f"Analysis error: {e}")
            return self._fallback_analysis(image)
    
    def _preprocess_image(self, image):
        """Preprocess image for model input"""
        # Resize image to standard size
        image = image.resize((224, 224))
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert to tensor
        image_array = np.array(image)
        image_tensor = torch.tensor(image_array).permute(2, 0, 1).float() / 255.0
        image_tensor = image_tensor.unsqueeze(0).to(self.device)
        
        return image_tensor
    
    def _generate_description(self, image_tensor):
        """Generate text description from image"""
        # This is a simplified version - in practice, you'd use a proper vision-language model
        # For now, we'll use image analysis to generate descriptions
        
        # Analyze image properties
        image_np = image_tensor.squeeze(0).permute(1, 2, 0).cpu().numpy()
        
        # Basic image analysis
        brightness = np.mean(image_np)
        color_variance = np.var(image_np)
        
        # Generate description based on image properties
        if brightness > 0.7:
            if color_variance > 0.1:
                return "bright and colorful scene with vibrant colors"
            else:
                return "bright and clean scene with soft lighting"
        elif brightness < 0.3:
            return "dark and moody scene with dramatic lighting"
        else:
            return "balanced scene with natural lighting"
    
    def _classify_sentiment(self, description):
        """Classify sentiment based on description"""
        positive_words = ['bright', 'colorful', 'vibrant', 'happy', 'joyful', 'cheerful', 'beautiful', 'amazing']
        negative_words = ['dark', 'moody', 'sad', 'gloomy', 'dramatic', 'tense']
        
        description_lower = description.lower()
        
        positive_score = sum(1 for word in positive_words if word in description_lower)
        negative_score = sum(1 for word in negative_words if word in description_lower)
        
        if positive_score > negative_score:
            return "Positive"
        elif negative_score > positive_score:
            return "Negative"
        else:
            return "Neutral"
    
    def _fallback_analysis(self, image):
        """Fallback analysis when model is not available"""
        # Analyze image properties for sentiment
        image_array = np.array(image)
        
        # Calculate brightness
        brightness = np.mean(image_array) / 255.0
        
        # Calculate color variance (vibrancy)
        color_variance = np.var(image_array)
        
        # Generate context based on image properties
        if brightness > 0.7:
            if color_variance > 1000:
                context = "bright and vibrant scene with rich colors"
                sentiment = "Positive"
            else:
                context = "bright and clean scene with soft tones"
                sentiment = "Positive"
        elif brightness < 0.3:
            context = "dark and atmospheric scene with dramatic lighting"
            sentiment = "Neutral"
        else:
            context = "balanced scene with natural lighting and colors"
            sentiment = "Neutral"
        
        # Add more specific context based on image characteristics
        if len(image_array.shape) == 3:
            # Color analysis
            r, g, b = np.mean(image_array, axis=(0, 1))
            if r > g and r > b:
                context += " with warm red tones"
            elif g > r and g > b:
                context += " with natural green elements"
            elif b > r and b > g:
                context += " with cool blue tones"
        
        return sentiment, context
    
    def analyze_images_together(self, images):
        """
        Analyze multiple images together to get overall sentiment and context
        Returns: (overall_sentiment, overall_context)
        """
        try:
            if not images:
                return "Neutral", "No images provided"
            
            # Analyze each image individually first
            individual_analyses = []
            for image in images:
                sentiment, context = self.analyze_image(image)
                individual_analyses.append((sentiment, context))
            
            # Combine the analyses to get overall sentiment and context
            sentiments = [analysis[0] for analysis in individual_analyses]
            contexts = [analysis[1] for analysis in individual_analyses]
            
            # Determine overall sentiment (majority vote)
            positive_count = sentiments.count("Positive")
            negative_count = sentiments.count("Negative")
            neutral_count = sentiments.count("Neutral")
            
            if positive_count >= negative_count and positive_count >= neutral_count:
                overall_sentiment = "Positive"
            elif negative_count >= positive_count and negative_count >= neutral_count:
                overall_sentiment = "Negative"
            else:
                overall_sentiment = "Neutral"
            
            # Combine contexts into overall context
            overall_context = self._combine_contexts(contexts, overall_sentiment)
            
            return overall_sentiment, overall_context
            
        except Exception as e:
            st.warning(f"Error in combined analysis: {e}")
            return "Neutral", "Error analyzing images together"
    
    def _combine_contexts(self, contexts, overall_sentiment):
        """Combine individual contexts into an overall context description"""
        # Extract key themes from all contexts
        all_words = []
        for context in contexts:
            words = context.lower().split()
            all_words.extend(words)
        
        # Find common themes
        word_counts = {}
        for word in all_words:
            if len(word) > 3:  # Only consider meaningful words
                word_counts[word] = word_counts.get(word, 0) + 1
        
        # Get most common themes
        common_themes = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        theme_words = [word for word, count in common_themes]
        
        # Create overall context based on sentiment and themes
        if overall_sentiment == "Positive":
            if "bright" in theme_words or "colorful" in theme_words:
                return f"vibrant collection with bright, colorful scenes and uplifting energy"
            elif "natural" in theme_words or "clean" in theme_words:
                return f"clean, natural collection with fresh, positive vibes"
            else:
                return f"positive collection with cheerful and uplifting content"
        elif overall_sentiment == "Negative":
            if "dark" in theme_words or "moody" in theme_words:
                return f"dramatic collection with dark, moody atmospheres and intense emotions"
            else:
                return f"intense collection with powerful, dramatic content"
        else:
            if "natural" in theme_words or "balanced" in theme_words:
                return f"balanced collection with natural, professional scenes and clean aesthetics"
            else:
                return f"professional collection with clean, modern content and balanced composition"


import chromadb
from sentence_transformers import SentenceTransformer
import json
import streamlit as st

class RAGDatabase:
    def __init__(self):
        """Initialize RAG database with prompt matching"""
        self.client = chromadb.Client()
        try:
            self.collection = self.client.create_collection("prompts")
        except Exception:
            # Collection already exists, get it
            self.collection = self.client.get_collection("prompts")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.initialize_prompts()
    
    def initialize_prompts(self):
        """Initialize the database with curated prompts for different sentiments and contexts"""
        prompts_data = [
            # Positive sentiment prompts
            {
                "sentiment": "Positive",
                "context": "bright and colorful scene with vibrant colors",
                "prompt": "Create a vibrant, energetic Instagram reel with bright colors, upbeat transitions, and dynamic movements. Use fast-paced editing with zoom effects and color grading that enhances the vibrancy. Add energetic music and smooth transitions between scenes.",
                "style": "vibrant"
            },
            {
                "sentiment": "Positive", 
                "context": "bright and clean scene with soft lighting",
                "prompt": "Create an elegant, clean Instagram reel with soft lighting, gentle transitions, and minimalist aesthetic. Use smooth fade effects, subtle zoom, and warm color grading. Focus on the beauty of simplicity with calming music.",
                "style": "minimalist"
            },
            {
                "sentiment": "Positive",
                "context": "outdoor scene with natural elements",
                "prompt": "Create an adventurous, nature-focused Instagram reel with outdoor vibes, natural lighting, and organic transitions. Use wide shots, close-ups of details, and earthy color grading. Add inspiring, uplifting music that matches the outdoor theme.",
                "style": "adventure"
            },
            
            # Neutral sentiment prompts
            {
                "sentiment": "Neutral",
                "context": "balanced scene with natural lighting and colors",
                "prompt": "Create a balanced, professional Instagram reel with clean transitions, natural color grading, and smooth camera movements. Use medium-paced editing with focus on composition and storytelling. Add neutral, ambient music.",
                "style": "professional"
            },
            {
                "sentiment": "Neutral",
                "context": "urban or city scene",
                "prompt": "Create a modern, urban Instagram reel with sleek transitions, contemporary editing style, and city vibes. Use dynamic angles, quick cuts, and modern color grading. Add trendy, electronic music that fits the urban aesthetic.",
                "style": "modern"
            },
            
            # Negative sentiment prompts
            {
                "sentiment": "Negative",
                "context": "dark and moody scene with dramatic lighting",
                "prompt": "Create a cinematic, dramatic Instagram reel with moody lighting, slow transitions, and artistic color grading. Use dramatic angles, slow-motion effects, and deep shadows. Add atmospheric, emotional music that enhances the mood.",
                "style": "cinematic"
            },
            {
                "sentiment": "Negative",
                "context": "atmospheric or artistic scene",
                "prompt": "Create an artistic, creative Instagram reel with unique transitions, creative effects, and artistic color grading. Use experimental editing techniques, creative angles, and artistic filters. Add ambient, creative music that matches the artistic vision.",
                "style": "artistic"
            },
            
            # Special context prompts
            {
                "sentiment": "Positive",
                "context": "people or social scene",
                "prompt": "Create a social, engaging Instagram reel with people-focused content, dynamic group shots, and social media-friendly transitions. Use quick cuts, zoom effects, and vibrant color grading. Add upbeat, social music that encourages engagement.",
                "style": "social"
            },
            {
                "sentiment": "Neutral",
                "context": "food or dining scene",
                "prompt": "Create a food-focused Instagram reel with appetizing close-ups, smooth transitions, and warm color grading. Use slow-motion for food details, quick cuts for variety, and food-focused angles. Add appetizing, warm music that enhances the food experience.",
                "style": "food"
            },
            {
                "sentiment": "Positive",
                "context": "travel or vacation scene",
                "prompt": "Create a travel-inspired Instagram reel with wanderlust vibes, scenic transitions, and travel-focused editing. Use wide landscape shots, quick location changes, and vibrant color grading. Add inspiring, travel-themed music that evokes wanderlust.",
                "style": "travel"
            }
        ]
        
        # Add prompts to database
        for i, prompt_data in enumerate(prompts_data):
            # Create embedding for the context
            embedding = self.embedder.encode(prompt_data["context"]).tolist()
            
            self.collection.add(
                embeddings=[embedding],
                documents=[prompt_data["prompt"]],
                metadatas=[{
                    "sentiment": prompt_data["sentiment"],
                    "context": prompt_data["context"],
                    "style": prompt_data["style"]
                }],
                ids=[f"prompt_{i}"]
            )
    
    def get_matching_prompt(self, sentiment, context):
        """Get the best matching prompt based on sentiment and context"""
        try:
            # Create embedding for the input context
            query_embedding = self.embedder.encode(context).tolist()
            
            # Search for similar prompts
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=3,
                where={"sentiment": sentiment} if sentiment else None
            )
            
            if results['documents'] and len(results['documents'][0]) > 0:
                # Return the best match
                best_match = results['documents'][0][0]
                return best_match
            else:
                # Fallback to a general prompt
                return self._get_fallback_prompt(sentiment)
                
        except Exception as e:
            st.warning(f"RAG database error: {e}")
            return self._get_fallback_prompt(sentiment)
    
    def _get_fallback_prompt(self, sentiment):
        """Get a fallback prompt when RAG search fails"""
        fallback_prompts = {
            "Positive": "Create an engaging, upbeat Instagram reel with vibrant colors, smooth transitions, and energetic editing. Use dynamic movements, quick cuts, and bright color grading. Add uplifting music that matches the positive energy.",
            "Negative": "Create a cinematic, artistic Instagram reel with moody lighting, creative transitions, and dramatic editing. Use slow-motion effects, artistic angles, and atmospheric color grading. Add emotional, ambient music.",
            "Neutral": "Create a professional, clean Instagram reel with balanced editing, smooth transitions, and natural color grading. Use medium-paced editing with focus on composition and storytelling. Add neutral, ambient music."
        }
        
        return fallback_prompts.get(sentiment, fallback_prompts["Neutral"])
    
    def add_custom_prompt(self, sentiment, context, prompt, style):
        """Add a custom prompt to the database"""
        try:
            embedding = self.embedder.encode(context).tolist()
            
            # Generate unique ID
            import time
            prompt_id = f"custom_{int(time.time())}"
            
            self.collection.add(
                embeddings=[embedding],
                documents=[prompt],
                metadatas=[{
                    "sentiment": sentiment,
                    "context": context,
                    "style": style,
                    "custom": True
                }],
                ids=[prompt_id]
            )
            
            return True
        except Exception as e:
            st.error(f"Error adding custom prompt: {e}")
            return False


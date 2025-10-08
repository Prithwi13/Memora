import streamlit as st
import os
import tempfile
from PIL import Image
import base64
from sentiment_analyzer import SentimentAnalyzer
from rag_database import RAGDatabase
from video_generator import VideoGenerator
from config import GEMINI_API_KEY

# Page configuration
st.set_page_config(
    page_title="Memora - AI Photo to Reel Generator",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for classy, professional design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #8b5cf6 100%);
        padding: 3rem 2rem;
        border-radius: 24px;
        margin-bottom: 3rem;
        text-align: center;
        color: white;
        box-shadow: 0 25px 50px rgba(30, 58, 138, 0.3);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }
    
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 50%);
        pointer-events: none;
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .main-header p {
        font-size: 1.2rem;
        font-weight: 300;
        margin: 1rem 0 0 0;
        opacity: 0.9;
    }
    
    .steps-container {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 2rem;
        border-radius: 24px;
        margin: 2rem 0;
        border: 1px solid #e2e8f0;
        position: relative;
        overflow: hidden;
    }
    
    .steps-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899);
    }
    
    .steps-horizontal {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 1rem;
        position: relative;
    }
    
    .step-item {
        flex: 1;
        text-align: center;
        position: relative;
        padding: 1rem 0.5rem;
    }
    
    .step-item:not(:last-child)::after {
        content: '';
        position: absolute;
        top: 20px;
        right: -0.5rem;
        width: 2rem;
        height: 2px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        z-index: 1;
    }
    
    .step-number {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        margin: 0 auto 1rem auto;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
        position: relative;
        z-index: 2;
    }
    
    .step-content {
        text-align: center;
    }
    
    .step-title {
        font-size: 1rem;
        font-weight: 600;
        color: #1e293b;
        margin: 0 0 0.5rem 0;
        line-height: 1.3;
    }
    
    .step-description {
        font-size: 0.85rem;
        color: #64748b;
        margin: 0;
        line-height: 1.4;
    }
    
    .stFileUploader > div {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border: 2px dashed #3b82f6;
        border-radius: 20px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div:hover {
        border-color: #2563eb;
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.2);
    }
    
    .stFileUploader label {
        font-size: 1.1rem;
        font-weight: 600;
        color: #3b82f6;
    }
    
    .result-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        margin: 1.5rem 0;
        border: 1px solid #e2e8f0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem 2.5rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-4px) scale(1.05);
        box-shadow: 0 15px 35px rgba(59, 130, 246, 0.5);
        background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .sidebar .stSelectbox > div > div {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
    }
    
    .sidebar .stSlider > div > div > div {
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
    }
    
    .footer {
        text-align: center;
        color: #64748b;
        padding: 2rem;
        font-size: 0.9rem;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        margin-top: 2rem;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        height: 4px;
        border-radius: 2px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎬 Memora</h1>
        <p>Transform your photos into stunning Instagram reels with AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Step-by-step process - Horizontal 2025 Style
    st.markdown("""
    <div class="steps-container">
        <div class="steps-horizontal">
            <div class="step-item">
                <div class="step-number">1</div>
                <div class="step-content">
                    <div class="step-title">Upload</div>
                </div>
            </div>
            <div class="step-item">
                <div class="step-number">2</div>
                <div class="step-content">
                    <div class="step-title">Analyze</div>
                </div>
            </div>
            <div class="step-item">
                <div class="step-number">3</div>
                <div class="step-content">
                    <div class="step-title">Match</div>
                </div>
            </div>
            <div class="step-item">
                <div class="step-number">4</div>
                <div class="step-content">
                    <div class="step-title">Generate</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize components
    if 'sentiment_analyzer' not in st.session_state:
        st.session_state.sentiment_analyzer = SentimentAnalyzer()
    
    if 'rag_database' not in st.session_state:
        st.session_state.rag_database = RAGDatabase()
    
    if 'video_generator' not in st.session_state:
        st.session_state.video_generator = VideoGenerator()
    
    # Settings in main area
    st.markdown("### ⚙️ Settings")
    
    # Video duration - shorter default
    duration = st.slider(
        "⏱️ Duration (seconds)",
        min_value=10,
        max_value=30,
        value=15,
        step=5,
        help="Duration of the generated reel"
    )
    
    # Upload section - Single clean upload area
    st.markdown("### 📸 Upload Your Photos")
    
    uploaded_files = st.file_uploader(
        "Choose images to create your reel",
        type=['png', 'jpg', 'jpeg'],
        accept_multiple_files=True,
        help="Upload multiple photos to create a dynamic reel"
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} images uploaded successfully!")
        
        # Display uploaded images
        st.markdown("#### 📷 Image Preview")
        cols = st.columns(3)
        for i, uploaded_file in enumerate(uploaded_files[:6]):  # Show max 6 images
            with cols[i % 3]:
                image = Image.open(uploaded_file)
                st.image(image, caption=f"Image {i+1}", use_container_width=True)
        
        # Generate video section
        st.markdown("### 🎬 Generate Your Reel")
        
        if st.button("🚀 Create Instagram Reel", type="primary", use_container_width=True):
            with st.spinner("Step 2: Analyzing all images together with BERT5..."):
                # Analyze all images together for overall sentiment and context
                all_images = [Image.open(uploaded_file) for uploaded_file in uploaded_files]
                
                # Get overall sentiment and context for all images combined
                overall_sentiment, overall_context = st.session_state.sentiment_analyzer.analyze_images_together(all_images)
                
                # Get matching prompt from RAG database
                overall_prompt = st.session_state.rag_database.get_matching_prompt(overall_sentiment, overall_context)
                
                # Create analysis results with the same structure but using overall analysis
                analysis_results = []
                for uploaded_file in uploaded_files:
                    image = Image.open(uploaded_file)
                    analysis_results.append({
                        'image': image,
                        'sentiment': overall_sentiment,
                        'context': overall_context,
                        'prompt': overall_prompt
                    })
                
                st.success("✅ Step 2 Complete: Overall context generated from BERT5 model")
                
                # Display overall sentiment analysis results
                st.markdown("#### 🧠 Overall Sentiment Analysis")
                with st.container():
                    st.markdown(f"🎭 **Overall Sentiment:** {overall_sentiment}")
                    st.markdown(f"📝 **Overall Context:** {overall_context}")
                    st.markdown(f"🎯 **Matched Prompt:** {overall_prompt}")
                    st.markdown("---")
            
            with st.spinner("Step 3: Finding appropriate prompt from RAG database..."):
                st.success("✅ Step 3 Complete: Best prompts matched from RAG database")
            
            with st.spinner("Step 4: Generating video with Gemini and MoviePy..."):
                try:
                    # Generate video
                    video_path = st.session_state.video_generator.create_reel(
                        analysis_results,
                        music_style="Upbeat",  # Default music style
                        duration=duration,
                        style="Modern"  # Default video style
                    )
                    
                    if video_path:
                        st.success("🎉 Step 4 Complete: Your reel is ready!")
                        
                        # Display video
                        st.video(video_path)
                        
                        # Download button
                        with open(video_path, "rb") as file:
                            st.download_button(
                                label="📥 Download Reel",
                                data=file.read(),
                                file_name="my_instagram_reel.mp4",
                                mime="video/mp4"
                            )
                    else:
                        st.error("❌ Video generation failed. Please try again.")
                    
                except Exception as e:
                    st.error(f"❌ Error generating video: {str(e)}")
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>🎬 Memora - Powered by AI • Built with ❤️</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()


"""
Legal Clause Simplifier - Main Streamlit Application
A premium, futuristic web application for simplifying legal clauses using local AI.
"""

import streamlit as st
import streamlit.components.v1 as components
from typing import Optional
import logging

from model_loader import get_model_and_tokenizer, model_loader
from inference import create_inference_engine
from utils import (
    validate_clause,
    format_risk_level,
    get_risk_color,
    get_risk_emoji,
    format_explanation,
    estimate_reading_time,
    log_analysis,
    get_example_clauses
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Legal Clause Simplifier",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for premium glassmorphic design
def inject_custom_css():
    """Inject advanced CSS for glassmorphism, animations, and hide Streamlit defaults."""
    
    st.markdown("""
    <style>
    /* Import Inter font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Hide Streamlit defaults */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Smooth scrolling */
    html {
        scroll-behavior: smooth;
    }
    
    /* Root styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Main container background - deep navy to black gradient */
    .stApp {
        background: linear-gradient(180deg, #0a0f1e 0%, #020617 50%, #000000 100%);
        background-attachment: fixed;
    }
    
    /* Hero section entrance animation */
    @keyframes heroEntrance {
        0% {
            opacity: 0;
            transform: translateY(-30px);
        }
        100% {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        0% {
            opacity: 0;
        }
        100% {
            opacity: 1;
        }
    }
    
    @keyframes scaleIn {
        0% {
            opacity: 0;
            transform: scale(0.95);
        }
        100% {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    @keyframes pulseGlow {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.7;
        }
    }
    
    @keyframes shimmer {
        0% {
            background-position: -1000px 0;
        }
        100% {
            background-position: 1000px 0;
        }
    }
    
    /* Hero title animation */
    .hero-title {
        animation: heroEntrance 1.2s ease-out;
        font-size: 5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #e0e7ff 50%, #c7d2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 1rem;
        line-height: 1.1;
    }
    
    .hero-subtitle {
        animation: fadeIn 1.5s ease-out 0.3s both;
        font-size: 1.5rem;
        color: rgba(255, 255, 255, 0.6);
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 300;
    }
    
    .hero-badge {
        animation: scaleIn 0.8s ease-out;
        display: inline-block;
        padding: 0.5rem 1.5rem;
        background: rgba(99, 102, 241, 0.2);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 50px;
        color: rgba(168, 185, 247, 1);
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
    }
    
    /* Glassmorphism classes */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        padding: 2rem;
        animation: scaleIn 0.6s ease-out;
    }
    
    .glass-panel {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .glass-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    /* Risk-based styling */
    .risk-low {
        border: 2px solid rgba(16, 185, 129, 0.5);
        box-shadow: 0 0 40px rgba(16, 185, 129, 0.3),
                    inset 0 0 40px rgba(16, 185, 129, 0.1);
        animation: pulseGlow 3s infinite;
    }
    
    .risk-medium {
        border: 2px solid rgba(245, 158, 11, 0.5);
        box-shadow: 0 0 40px rgba(245, 158, 11, 0.3),
                    inset 0 0 40px rgba(245, 158, 11, 0.1);
        animation: pulseGlow 3s infinite;
    }
    
    .risk-high {
        border: 2px solid rgba(239, 68, 68, 0.5);
        box-shadow: 0 0 40px rgba(239, 68, 68, 0.3),
                    inset 0 0 40px rgba(239, 68, 68, 0.1);
        animation: pulseGlow 3s infinite;
    }
    
    .risk-badge-low {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.9), rgba(5, 150, 105, 0.9));
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 50px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.4);
    }
    
    .risk-badge-medium {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.9), rgba(217, 119, 6, 0.9));
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 50px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 4px 20px rgba(245, 158, 11, 0.4);
    }
    
    .risk-badge-high {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.9), rgba(220, 38, 38, 0.9));
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 50px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 4px 20px rgba(239, 68, 68, 0.4);
    }
    
    /* Custom textarea styling */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        color: rgba(255, 255, 255, 0.9) !important;
        font-size: 1rem !important;
        padding: 1rem !important;
        backdrop-filter: blur(8px);
        transition: all 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        background: rgba(255, 255, 255, 0.08) !important;
        border-color: rgba(99, 102, 241, 0.5) !important;
        box-shadow: 0 0 30px rgba(99, 102, 241, 0.3) !important;
    }
    
    /* Custom button styling */
    .stButton > button {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.8), rgba(139, 92, 246, 0.8)) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 16px !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        padding: 0.75rem 2rem !important;
        backdrop-filter: blur(16px);
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.4);
        transition: all 0.3s ease !important;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 12px 40px rgba(99, 102, 241, 0.6) !important;
        background: linear-gradient(135deg, rgba(99, 102, 241, 1), rgba(139, 92, 246, 1)) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) scale(0.98) !important;
    }
    
    /* Loading spinner */
    .loading-spinner {
        width: 60px;
        height: 60px;
        border: 4px solid rgba(99, 102, 241, 0.2);
        border-top: 4px solid rgba(99, 102, 241, 1);
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 2rem auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Text styling */
    .explanation-text {
        color: rgba(255, 255, 255, 0.85);
        font-size: 1.1rem;
        line-height: 1.8;
        font-weight: 400;
    }
    
    h1, h2, h3 {
        color: rgba(255, 255, 255, 0.95);
    }
    
    /* Example card */
    .example-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .example-card:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(99, 102, 241, 0.5);
        transform: translateX(5px);
    }
    
    /* Scroll reveal */
    .scroll-reveal {
        opacity: 0;
        transform: translateY(30px);
        animation: fadeUpIn 0.8s ease-out forwards;
    }
    
    @keyframes fadeUpIn {
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Feature icons */
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    /* Gradient text */
    .gradient-text {
        background: linear-gradient(135deg, #6366f1, #8b5cf6, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Info text */
    .info-text {
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)


def render_3d_scene():
    """Render a 3D scene using Spline."""
    
    spline_html = """
    <div style="width: 100%; height: 600px; border-radius: 24px; overflow: hidden; position: relative;">
        <iframe 
            src='https://my.spline.design/untitled-2e3a87f9f23c25f6c7b39f7b8f36e71e/' 
            frameborder='0' 
            width='100%' 
            height='100%'
            style='border: none; background: transparent;'>
        </iframe>
    </div>
    """
    
    components.html(spline_html, height=600)


def render_custom_loading():
    """Render custom loading animation."""
    
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0;">
        <div class="loading-spinner"></div>
        <p style="color: rgba(255, 255, 255, 0.6); margin-top: 1rem; font-size: 1.1rem;">
            🤖 Analyzing your clause with local AI...
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_hero_section():
    """Render the hero landing page section."""
    
    st.markdown("""
    <div style="text-align: center; padding: 4rem 0 6rem 0;">
        <div class="hero-badge">
            ✨ AI-Powered Legal Analysis
        </div>
        
        <h1 class="hero-title">
            Legal Clause<br/>Simplifier
        </h1>
        
        <p class="hero-subtitle">
            Transform complex rental agreement clauses into plain English<br/>
            with AI-powered risk assessment—completely local and private.
        </p>
        
        <div style="margin-top: 2rem;">
            <div style="display: inline-flex; gap: 1rem; align-items: center; justify-content: center;">
                <div class="glass-badge">
                    🔒 100% Private
                </div>
                <div class="glass-badge">
                    ⚡ Instant Analysis
                </div>
                <div class="glass-badge">
                    🎯 Risk Detection
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_risk_output(risk: str, explanation: str):
    """Render the risk output with dynamic styling."""
    
    risk_class = f"risk-{risk.lower()}"
    badge_class = f"risk-badge-{risk.lower()}"
    emoji = get_risk_emoji(risk)
    
    st.markdown(f"""
    <div class="glass-card {risk_class} scroll-reveal">
        <div class="{badge_class}">
            {emoji} {risk} Risk
        </div>
        
        <h3 style="margin-top: 2rem; margin-bottom: 1rem; color: rgba(255, 255, 255, 0.95);">
            Plain English Explanation
        </h3>
        
        <p class="explanation-text">
            {explanation}
        </p>
        
        <div class="info-text" style="margin-top: 2rem;">
            📖 Reading time: ~{estimate_reading_time(explanation)} min
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_features_section():
    """Render the features section."""
    
    st.markdown("""
    <div style="margin-top: 6rem;">
        <h2 style="text-align: center; margin-bottom: 3rem; font-size: 2.5rem;" class="gradient-text">
            How It Works
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="glass-panel scroll-reveal" style="text-align: center; height: 100%;">
            <div class="feature-icon">🔒</div>
            <h3>100% Private</h3>
            <p style="color: rgba(255, 255, 255, 0.6);">
                All processing happens locally on your machine. 
                Your legal clauses never leave your device.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-panel scroll-reveal" style="text-align: center; height: 100%;">
            <div class="feature-icon">✨</div>
            <h3>AI-Powered</h3>
            <p style="color: rgba(255, 255, 255, 0.6);">
                Fine-tuned Gemma 3 270M model specifically trained 
                on rental agreement clauses.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="glass-panel scroll-reveal" style="text-align: center; height: 100%;">
            <div class="feature-icon">⚖️</div>
            <h3>Risk Assessment</h3>
            <p style="color: rgba(255, 255, 255, 0.6);">
                Automatic risk level detection classifies clauses as 
                Low, Medium, or High risk.
            </p>
        </div>
        """, unsafe_allow_html=True)


@st.cache_resource
def load_model_cached():
    """Load model with caching for better performance."""
    try:
        model, tokenizer = get_model_and_tokenizer("./model")
        device = model_loader.device
        inference_engine = create_inference_engine(model, tokenizer, device)
        return inference_engine, None
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        return None, str(e)


def main():
    """Main application function."""
    
    # Inject custom CSS
    inject_custom_css()
    
    # Render hero section
    render_hero_section()
    
    # Main application layout
    st.markdown('<div style="margin-top: 4rem;"></div>', unsafe_allow_html=True)
    
    # Create two-column layout
    col_left, col_right = st.columns([1, 1], gap="large")
    
    with col_left:
        # 3D visualization
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🎨 3D Visualization")
        render_3d_scene()
        
        st.markdown("""
        <div class="glass-panel" style="margin-top: 1rem;">
            <h4 style="margin: 0; color: rgba(255, 255, 255, 0.9);">Local AI Model</h4>
            <p style="color: rgba(255, 255, 255, 0.6); margin: 0.5rem 0 0 0; font-size: 0.95rem;">
                Powered by Gemma 3 270M running locally. Complete privacy guaranteed.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_right:
        # Input section
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📝 Paste Your Rental Clause")
        
        # Clause input
        clause_text = st.text_area(
            "Enter legal clause",
            height=250,
            placeholder="Example: The tenant must provide written notice of at least 30 days prior to vacating the premises...",
            label_visibility="collapsed"
        )
        
        # Analyze button
        analyze_button = st.button("✨ Simplify Clause", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Initialize session state
        if 'result' not in st.session_state:
            st.session_state.result = None
        
        # Process input
        if analyze_button:
            # Validate input
            is_valid, error_msg = validate_clause(clause_text)
            
            if not is_valid:
                st.markdown(f"""
                <div class="glass-panel" style="border-color: rgba(239, 68, 68, 0.5);">
                    <p style="color: rgba(239, 68, 68, 1); margin: 0;">
                        ⚠️ {error_msg}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Load model
                with st.spinner(""):
                    render_custom_loading()
                    inference_engine, error = load_model_cached()
                
                if error:
                    st.error(f"Failed to load model: {error}")
                    st.info("Please ensure your model is placed in the ./model/ directory")
                else:
                    # Run inference
                    try:
                        with st.spinner(""):
                            result = inference_engine.simplify_clause(clause_text)
                            st.session_state.result = result
                            log_analysis(clause_text, result['risk'], result['explanation'])
                    except Exception as e:
                        logger.error(f"Inference failed: {str(e)}")
                        st.error(f"Analysis failed: {str(e)}")
        
        # Display result
        if st.session_state.result:
            st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
            risk = format_risk_level(st.session_state.result['risk'])
            explanation = format_explanation(st.session_state.result['explanation'])
            render_risk_output(risk, explanation)
        else:
            # Empty state
            st.markdown("""
            <div class="glass-panel scroll-reveal" style="text-align: center; margin-top: 2rem; padding: 3rem 2rem;">
                <div style="font-size: 4rem; margin-bottom: 1rem; opacity: 0.3;">⚖️</div>
                <p style="color: rgba(255, 255, 255, 0.4); margin: 0;">
                    Enter a rental clause above to get started
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    # Features section
    render_features_section()
    
    # Example clauses section
    st.markdown('<div style="margin-top: 6rem;"></div>', unsafe_allow_html=True)
    
    with st.expander("📚 Try Example Clauses"):
        examples = get_example_clauses()
        for example in examples:
            if st.button(f"{example['title']}", key=example['title'], use_container_width=True):
                st.session_state.example_clause = example['clause']
                st.rerun()
    
    # Footer
    st.markdown("""
    <div style="margin-top: 6rem; padding: 3rem 0; text-align: center; border-top: 1px solid rgba(255, 255, 255, 0.1);">
        <p style="color: rgba(255, 255, 255, 0.4); font-size: 0.9rem;">
            Legal Clause Simplifier • Powered by Gemma 3 270M • 100% Local & Private
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

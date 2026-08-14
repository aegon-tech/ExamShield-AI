import streamlit as st

def inject_enterprise_theme():
    """Injects custom enterprise CSS theme, overriding Streamlit's native DOM."""
    st.markdown("""
    <style>
    /* 1. Typography & Global Theme */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #0B0F19 !important;
        color: #e2e8f0 !important;
    }

    /* 2. Cleanliness - Hide default elements */
    #MainMenu, footer, header[data-testid="stHeader"] {
        visibility: hidden !important;
        height: 0 !important;
        display: none !important;
    }

    /* 3. Surface Panels - Sidebar Background */
    [data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    /* 4. Custom Navigation Sidebar (Overriding stRadio) */
    [data-testid="stSidebar"] div[role="radiogroup"] {
        display: flex;
        flex-direction: column;
        gap: 12px;
    }
    
    [data-testid="stSidebar"] div[role="radiogroup"] > label {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        padding: 14px 16px !important;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        margin: 0 !important;
        display: flex;
        align-items: center;
    }
    
    /* Hide the native radio circle */
    [data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }
    
    /* Style the radio label text */
    [data-testid="stSidebar"] div[role="radiogroup"] > label > div:last-child {
        margin-left: 0 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        color: #94a3b8 !important;
    }
    
    /* Hover State for Radio Items */
    [data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
        transform: translateX(8px) !important;
        background: rgba(255, 255, 255, 0.05) !important;
        border-color: rgba(99, 102, 241, 0.4) !important;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.15) !important;
    }
    
    [data-testid="stSidebar"] div[role="radiogroup"] > label:hover > div:last-child {
        color: #e2e8f0 !important;
    }
    
    /* Active State (Pill) using :has() pseudo-class */
    [data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {
        transform: translateX(8px) !important;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(139, 92, 246, 0.15)) !important;
        border-color: #8B5CF6 !important;
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.25) !important;
    }
    
    [data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) > div:last-child {
        color: #ffffff !important;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.3) !important;
    }

    /* 5. Interactive Components - File Uploader Dropzone */
    [data-testid="stFileUploadDropzone"] {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 2px dashed rgba(139, 92, 246, 0.3) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
        padding: 32px !important;
    }
    
    [data-testid="stFileUploadDropzone"]:hover {
        background: rgba(99, 102, 241, 0.08) !important;
        border-color: #8B5CF6 !important;
        box-shadow: 0 0 25px rgba(139, 92, 246, 0.15) !important;
    }
    
    [data-testid="stFileUploadDropzone"] * {
        color: #e2e8f0 !important;
    }

    /* 6. Glowing Gradient Buttons */
    [data-testid="stButton"] button[kind="primary"],
    [data-testid="stDownloadButton"] button[kind="primary"],
    [data-testid="stDownloadButton"] button[kind="secondary"] {
        background: linear-gradient(135deg, #6366F1, #8B5CF6) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.6rem 1.8rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
    }
    
    [data-testid="stButton"] button[kind="primary"]:hover,
    [data-testid="stDownloadButton"] button[kind="primary"]:hover,
    [data-testid="stDownloadButton"] button[kind="secondary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.5) !important;
    }

    /* Secondary Buttons (Glassmorphism Pill) */
    [data-testid="stButton"] button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #e2e8f0 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 50px !important;
        font-weight: 500 !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stButton"] button[kind="secondary"]:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: #8B5CF6 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(139, 92, 246, 0.2) !important;
        color: white !important;
    }

    /* 7. Dark Glassmorphism Inputs */
    [data-testid="stTextInput"] input, 
    [data-testid="stTextArea"] textarea {
        background-color: rgba(17, 24, 39, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #FFFFFF !important;
        backdrop-filter: blur(8px) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stTextInput"] input:focus, 
    [data-testid="stTextArea"] textarea:focus {
        border-color: #8B5CF6 !important;
        box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.3) !important;
    }
    
    /* Input Labels */
    .stTextInput label p, .stTextArea label p, .stFileUploader label p {
        color: #cbd5e1 !important;
        font-weight: 500 !important;
    }

    /* 8. Layout Structure - Modern Container Cards */
    [data-testid="column"] {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1.5rem;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    [data-testid="column"]:hover {
        border-color: rgba(255, 255, 255, 0.1);
        background: rgba(255, 255, 255, 0.03);
    }

    /* Hero Banner Container Base */
    .hero-container {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.4) 0%, rgba(15, 23, 42, 0.7) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(12px);
        position: relative;
        overflow: hidden;
    }
    
    .hero-container::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 3px;
        background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
    }

    /* Logo & Branding Vectors */
    .logo-badge-container {
        width: 52px;
        height: 52px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(168, 85, 247, 0.1) 100%);
        border: 1px solid rgba(129, 140, 248, 0.35);
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 25px rgba(99, 102, 241, 0.25), inset 0 1px 1px rgba(255, 255, 255, 0.2);
    }

    .brand-title-wrap {
        display: flex;
        align-items: center;
        gap: 18px;
    }

    .brand-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #ffffff 30%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1;
    }

    .brand-ai-tag {
        background: linear-gradient(135deg, #6366f1, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .pulse-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #10b981;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.05em;
    }
    
    .pulse-badge .dot {
        width: 8px;
        height: 8px;
        background-color: #10b981;
        border-radius: 50%;
        box-shadow: 0 0 10px #10b981;
    }
    
    /* Text Overrides */
    h1, h2, h3, h4, h5, h6 { color: #f8fafc !important; }
    p, stMarkdown { color: #cbd5e1 !important; }
    
    </style>
    """, unsafe_allow_html=True)

def render_header_banner():
    """Renders the top branding header with vector shield and status indicator."""
    st.markdown("""
    <div class="hero-container">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
            <div class="brand-title-wrap">
                <div class="logo-badge-container">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 2L3 7V12C3 17.52 6.84 22.18 12 23.5C17.16 22.18 21 17.52 21 12V7L12 2Z" 
                              fill="url(#shield-fill)" stroke="url(#shield-border)" stroke-width="1.5"/>
                        <path d="M12 6L6 9.33V12C6 15.68 8.56 18.79 12 19.67C15.44 18.79 18 15.68 18 12V9.33L12 6Z" 
                              stroke="url(#shield-inner)" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>
                        <defs>
                            <linearGradient id="shield-fill" x1="3" y1="2" x2="21" y2="23.5" gradientUnits="userSpaceOnUse">
                                <stop stop-color="#6366F1" stop-opacity="0.4"/>
                                <stop offset="1" stop-color="#A855F7" stop-opacity="0.1"/>
                            </linearGradient>
                            <linearGradient id="shield-border" x1="3" y1="2" x2="21" y2="23.5" gradientUnits="userSpaceOnUse">
                                <stop stop-color="#818CF8"/>
                                <stop offset="0.5" stop-color="#C084FC"/>
                                <stop offset="1" stop-color="#6366F1"/>
                            </linearGradient>
                            <linearGradient id="shield-inner" x1="6" y1="6" x2="18" y2="19.67" gradientUnits="userSpaceOnUse">
                                <stop stop-color="#38BDF8"/>
                                <stop offset="1" stop-color="#818CF8"/>
                            </linearGradient>
                        </defs>
                    </svg>
                </div>
                <div>
                    <h1 class="brand-title">ExamShield <span class="brand-ai-tag">AI</span></h1>
                    <p style="color: #94a3b8; margin-top: 4px; font-size: 0.9rem; font-weight: 500;">Steganographic Forensic Watermarking & In-Memory AI Suite</p>
                </div>
            </div>
            <div class="pulse-badge">
                <span class="dot"></span> SECURE IN-MEMORY ENGINE
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
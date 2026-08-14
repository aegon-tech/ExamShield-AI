"""
app.py - ExamShield AI Streamlit Application Interface
"""

import os
import streamlit as st

# Modern Google GenAI SDK Import
try:
    from google import genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

from ui_components import inject_enterprise_theme, render_header_banner
from pdf_engine import (
    embed_watermark_stream,
    batch_watermark_memory,
    extract_watermark_stream,
    text_to_pdf_stream,
    PDFEngineError
)

# Page Setup
st.set_page_config(
    page_title="ExamShield AI | Enterprise Security",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Theme and Render Header
inject_enterprise_theme()
render_header_banner()

# Initialize Session State
if "ai_generated_text" not in st.session_state:
    st.session_state["ai_generated_text"] = ""
if "ai_current_set" not in st.session_state:
    st.session_state["ai_current_set"] = ""

# Sidebar Navigation
st.sidebar.title("🛡️ Modules")
option = st.sidebar.radio(
    "Select Operation",
    [
        "📄 Single Paper Watermarker",
        "📦 Batch Center Generator",
        "🔍 Forensic Leak Detector",
        "🤖 AI Question Set Generator"
    ]
)

# ------------------------------------------------------------------------------
# 1. Single Paper Watermarker
# ------------------------------------------------------------------------------
if option == "📄 Single Paper Watermarker":
    st.subheader("📄 Single Paper Watermarker")
    st.caption("Embed an invisible forensic watermark directly into memory.")

    col1, col2 = st.columns([2, 1])
    with col1:
        uploaded_pdf = st.file_uploader("Upload Master PDF Paper", type=["pdf"])
    with col2:
        st.markdown("### Security Parameters")
        center_code = st.text_input("Enter Secret Center Code", "GKP_101")
        
    if uploaded_pdf and center_code:
        if st.button("🔒 Embed Forensic Watermark", type="primary"):
            with st.spinner("Processing in memory..."):
                try:
                    pdf_bytes = uploaded_pdf.getvalue()
                    watermarked_pdf = embed_watermark_stream(pdf_bytes, center_code)
                    
                    st.success("✅ Watermark embedded successfully!")
                    st.download_button(
                        label="⬇️ Download Watermarked PDF",
                        data=watermarked_pdf,
                        file_name=f"Secured_{center_code}.pdf",
                        mime="application/pdf"
                    )
                except PDFEngineError as err:
                    st.error(f"Processing Error: {str(err)}")

# ------------------------------------------------------------------------------
# 2. Batch Center Generator
# ------------------------------------------------------------------------------
elif option == "📦 Batch Center Generator":
    st.subheader("📦 Batch Center Generator")
    st.caption("Batch process exam papers completely in memory.")

    # Rendered as cards natively by CSS targetting Streamlit layout blocks
    col1, col2 = st.columns(2)
    with col1:
        uploaded_pdf = st.file_uploader("Upload Master PDF Paper", type=["pdf"], key="batch_pdf")
    with col2:
        uploaded_csv = st.file_uploader("Upload Center Mapping CSV (Columns: code, filename)", type=["csv"])

    if uploaded_pdf and uploaded_csv:
        if st.button("🚀 Process Batch", type="primary"):
            with st.spinner("Generating center papers and ZIP in memory..."):
                try:
                    zip_data, summary = batch_watermark_memory(uploaded_pdf.getvalue(), uploaded_csv.getvalue())
                    
                    st.success(f"✅ Batch completed! Processed: {summary['success']}/{summary['total']}")
                    if summary['failed'] > 0:
                        st.warning(f"Failed rows: {summary['failed']}")

                    st.download_button(
                        label="⬇️ Download All Center Papers (.ZIP)",
                        data=zip_data,
                        file_name="ExamShield_Distribution_Package.zip",
                        mime="application/zip"
                    )
                except PDFEngineError as err:
                    st.error(f"Batch Processing Error: {str(err)}")

# ------------------------------------------------------------------------------
# 3. Forensic Leak Detector
# ------------------------------------------------------------------------------
elif option == "🔍 Forensic Leak Detector":
    st.subheader("🔍 Forensic Leak Detector")
    st.caption("Trace leaked exam papers back to the specific origin center.")

    col1, col2 = st.columns([2, 1])
    with col1:
        leaked_pdf = st.file_uploader("Upload Leaked / Recovered PDF Paper", type=["pdf"])

    if leaked_pdf:
        if st.button("🕵️ Trace Watermark", type="primary"):
            with st.spinner("Analyzing forensic payload..."):
                try:
                    result = extract_watermark_stream(leaked_pdf.getvalue())
                    if result["detected"]:
                        st.error(f"🚨 WATERMARK DETECTED! Origin Center: **{result['code']}**")
                        st.json(result)
                    else:
                        st.success("✅ No Forensic Watermark Detected in this document.")
                except PDFEngineError as err:
                    st.error(f"Analysis Error: {str(err)}")

# ------------------------------------------------------------------------------
# 4. AI Question Set Generator
# ------------------------------------------------------------------------------
elif option == "🤖 AI Question Set Generator":
    st.subheader("🤖 AI Question Set Generator")
    st.caption("Generate variant question papers using Gemini AI.")

    if not GENAI_AVAILABLE:
        st.error("Google GenAI SDK is not installed (`pip install google-genai`).")

    # Cascading Secrets Management
    api_key = ""
    try:
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY", "")

    if not api_key:
        api_key = st.text_input("Gemini API Key", type="password")

    input_text = st.text_area("Paste Base Syllabus or Sample Questions", height=150)

    # UI columns auto-converted to glass cards
    col1, col2, col3 = st.columns(3)
    target_set = None
    if col1.button("✨ Generate Set A"): target_set = "Set A"
    if col2.button("✨ Generate Set B"): target_set = "Set B"
    if col3.button("✨ Generate Set C"): target_set = "Set C"

    if target_set and api_key and input_text:
        with st.spinner(f"Generating {target_set} via Gemini AI..."):
            try:
                client = genai.Client(api_key=api_key)
                prompt = f"Act as an expert examiner. Generate variant {target_set} based on this input:\n\n{input_text}"
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                
                # Persist generated state
                st.session_state["ai_generated_text"] = response.text
                st.session_state["ai_current_set"] = target_set
            except Exception as e:
                st.error(f"Error generating AI set: {str(e)}")

    # Persistent UI Block for Download
    if st.session_state["ai_generated_text"]:
        st.subheader(f"Generated Paper ({st.session_state['ai_current_set']})")
        st.text_area("Preview Output", st.session_state["ai_generated_text"], height=200)

        pdf_bytes = text_to_pdf_stream(st.session_state["ai_generated_text"])
        st.download_button(
            label=f"⬇️ Download {st.session_state['ai_current_set']} PDF",
            data=pdf_bytes,
            file_name=f"Exam_{st.session_state['ai_current_set']}.pdf",
            mime="application/pdf"
        )
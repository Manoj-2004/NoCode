import streamlit as st
import os
import shutil
from transcriber import transcribe_audio
from codegen import generate_ui_code
import streamlit.components.v1 as components
from zipfile import ZipFile

# PAGE CONFIG
st.set_page_config(
    page_title="ZeroCode - Voice to UI Code Generator",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CUSTOM CSS 
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(to right, #e0e7ff, #f0f9ff);
    }

    .block-container {
        padding: 2rem 2rem 2rem 2rem;
        border-radius: 20px;
    }

    h1, h2, h3, .stMarkdown {
        color: #1e3a8a;
    }

    .stTextArea, .stFileUploader, .stButton, .stDownloadButton {
        background-color: #ffffffcc !important;
        border-radius: 14px !important;
        padding: 1rem !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
        margin-bottom: 1rem;
    }

    .stButton>button, .stDownloadButton>button {
        background: #6366f1 !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        transition: 0.3s ease-in-out;
    }

    .stButton>button:hover, .stDownloadButton>button:hover {
        background: #4f46e5 !important;
    }

    .stAudio {
        margin-top: 1rem;
        margin-bottom: 1.5rem;
    }

    hr {
        margin-top: 2rem;
        margin-bottom: 2rem;
        border: none;
        height: 1px;
        background: #dbeafe;
    }
    </style>
""", unsafe_allow_html=True)

# TITLE 
st.markdown("<h1 style='text-align: center;'>🎨 ZEROCODE</h1>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; font-size: 18px; margin-top: -10px; margin-bottom: 1rem;'>
A local, private, and <b>voice-powered frontend UI generator</b>.<br>
Type or talk, and get production-ready UI code.
</div>
""", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# TEXT PROMPT 
st.subheader("📝 Text Prompt")
text_prompt = st.text_area("Describe the UI you want:", placeholder="e.g., I want an aesthetic landing page with a login form.")

# VOICE INPUT 
st.subheader("🎙️ Upload a Voice Recording (Optional)")
uploaded_audio = st.file_uploader("Upload a `.wav` file", type=["wav"])

# PROCESS VOICE 
final_prompt = None

if uploaded_audio:
    os.makedirs("temp_audio", exist_ok=True)
    audio_path = "temp_audio/uploaded.wav"

    with open(audio_path, "wb") as f:
        f.write(uploaded_audio.read())

    st.audio(audio_path, format="audio/wav")

    if st.button("🚀 Transcribe Voice Prompt"):
        with st.spinner("Transcribing..."):
            try:
                final_prompt = transcribe_audio(audio_path)
                st.success("Transcription Successful!")
                st.markdown(f"**🗣️ Transcribed Prompt:** `{final_prompt}`")
            except Exception as e:
                st.error(f"Transcription failed: {e}")

#FALLBACK TO TEXT 
if not final_prompt and text_prompt:
    final_prompt = text_prompt.strip()
    st.markdown(f"✅ Using typed prompt: `{final_prompt}`")

# GENERATE CODE 
if final_prompt and st.button("✨ Generate UI Code"):
    with st.spinner("Generating frontend code using LLaMA..."):
        try:
            html_code = generate_ui_code(final_prompt)
            st.session_state["generated_code"] = html_code
            st.success("✅ Code generated successfully!")
        except Exception as e:
            st.error(f"Code generation failed: {e}")

# PREVIEW UI 
if "generated_code" in st.session_state:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("🔍 Preview Your UI")
    components.html(st.session_state["generated_code"], height=600, scrolling=True)

    # DOWNLOAD ZIP
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("📦 Download Code")

    zip_dir = "generated_code"
    zip_file = "generated_ui.zip"
    os.makedirs(zip_dir, exist_ok=True)

    with open(os.path.join(zip_dir, "index.html"), "w") as f:
        f.write(st.session_state["generated_code"])

    with ZipFile(zip_file, "w") as zipf:
        zipf.write(os.path.join(zip_dir, "index.html"), arcname="index.html")

    with open(zip_file, "rb") as f:
        st.download_button("📁 Download Code as ZIP", f, file_name="zerocode_ui.zip", mime="application/zip")

    shutil.rmtree(zip_dir, ignore_errors=True)
    os.remove(zip_file)
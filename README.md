# 🎨 NoCode UI: AI-Powered Text & Voice to Frontend Generator

NoCode UI is an innovative, localized, and privacy-first web application that transforms spoken or written descriptions into instantly deployable frontend components. The system allows developers and designers to conceptualize a user interface using natural language and immediately receive production-ready HTML, CSS, and JavaScript. 🚀

---

## 🚀 Key Capabilities

*   **Acoustic Input Processing 🎙️**: Submit UI concepts via audio uploads (`.wav` format), which are parsed and translated into actionable text prompts utilizing OpenAI's Whisper pipeline.
*   **Textual Specifications 📝**: Directly type detailed interface requirements into an interactive console.
*   **Intelligent Code Synthesizer 💻**: Leverages Groq's high-speed LLaMA inference engine to generate clean, semantic frontend markup and styling.
*   **Real-time Render Preview 👀**: View live rendering of the compiled frontend design directly within the application dashboard.
*   **Exportable Bundles 📦**: Download the finalized assets as an isolated workspace ZIP container, featuring an indexed HTML ecosystem ready for staging.

---

## 🗂️ Project Architecture

*   **`app.py`**: The application kernel, housing the Streamlit configuration, user interaction layers, and rendering nodes.
*   **`transcriber.py`**: Manages the local machine learning pipeline for speech-to-text decoding using Whisper models.
*   **`codegen.py`**: Controls the structural prompt templates and handles upstream streaming API requests to Groq.
*   **`static/`**: Storage directory designated for localized assets, style elements, or media components.
*   **`requirements.txt`**: Manifest locking the specific Python library versions required to host the ecosystem.

---

## ⚙️ Environment Prerequisites

*   Python 3.8+ runtime environment 🐍
*   A modern IDE environment (e.g., Cursor, VS Code)
*   An active [Groq Cloud Platform API Key 🔑](https://groq.com/) for LLM processing nodes.

---

## 🛠️ Step-by-Step Deployment Guide

### 1. Initialize an Isolated Environment 🌱

#### Unix/macOS Terminals:
```bash
python3 -m venv venv
source venv/bin/activate
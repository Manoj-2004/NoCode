import requests
import os

# Load Groq API key from environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def generate_ui_code(user_prompt: str) -> str:
    """
    Sends the user prompt to Groq LLaMA 3 and returns the generated HTML/CSS/JS code.
    """
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY environment variable not set.")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    system_prompt = (
        "You are a professional frontend developer. "
        "Generate **only** full, well-structured, and minimalistic HTML code (with inline CSS and JS if needed) "
        "for the given UI requirement. Ensure:\n"
        "- It is mobile responsive.\n"
        "- CSS is either inline or in a `<style>` block.\n"
        "- JavaScript is embedded in a `<script>` block.\n"
        "- Use modern HTML5 and CSS3 standards.\n"
        "- Do NOT include explanations, markdown, or comments — only clean code inside `<html>...</html>`."
    )

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 4096,
        "top_p": 1,
        "stop": None
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise RuntimeError(f"Groq API failed: {response.status_code} - {response.text}")

    output = response.json()["choices"][0]["message"]["content"].strip()

    # Sanity check: Ensuring output is valid HTML 
    if not output.lower().startswith("<!doctype") and "<html" not in output:
        raise ValueError("Generated output doesn't look like valid HTML. Got:\n" + output[:200])

    return output
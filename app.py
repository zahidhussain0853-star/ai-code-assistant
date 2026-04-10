from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

app = Flask(__name__)

API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Store chat history (limit size later)
chat_history = []

# -------------------------------
# AI Function
# -------------------------------
def ask_ai(messages):
    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json={
                "model": "openrouter/auto",
                "messages": messages
            },
            timeout=30
        )

        response.raise_for_status()  # raises error if bad response
        result = response.json()

        return result["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        return f"API Error: {str(e)}"
    except Exception:
        return "Error: Could not process response"

# -------------------------------
# Routes
# -------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    global chat_history

    if request.method == "POST":
        user_input = request.form.get("user_input")

        if user_input:
            # Add system message once
            if not chat_history:
                chat_history.append({
                    "role": "system",
                    "content": "You are a helpful coding assistant. Give clean code and short explanations."
                })

            # Add user message
            chat_history.append({"role": "user", "content": user_input})

            # Limit history (important for performance)
            chat_history = chat_history[-10:]

            # Get AI response
            ai_response = ask_ai(chat_history)

            # Add AI response
            chat_history.append({"role": "assistant", "content": ai_response})

    return render_template("index.html", chat=chat_history)

# -------------------------------
# Run App
# -------------------------------
if __name__ == "__main__":
    # Render requires this config
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
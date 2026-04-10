from flask import Flask, render_template, request
import requests

from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
#print("API KEY APP:", API_KEY)

app = Flask(__name__)

API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Store chat history
chat_history = []

def ask_ai(messages):
    response = requests.post(
        API_URL,
        headers=headers,
        json={
            "model": "openrouter/auto",
            "messages": messages
        }
    )

    try:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except:
        return "Error: Could not get response"


@app.route("/", methods=["GET", "POST"])
def index():
    global chat_history

    if request.method == "POST":
        user_input = request.form.get("user_input")

        # Add user message
        chat_history.append({"role": "user", "content": user_input})

        # Add system instruction (only once at start)
        if len(chat_history) == 1:
            chat_history.insert(0, {
                "role": "system",
                "content": "You are a helpful coding assistant. Give clear code and short explanations."
            })

        # Get AI response
        ai_response = ask_ai(chat_history)

        # Add AI response
        chat_history.append({"role": "assistant", "content": ai_response})

    return render_template("index.html", chat=chat_history)


if __name__ == "__main__":
    app.run(debug=True)
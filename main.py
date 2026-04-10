import requests
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
#print("API KEY MAIN:", os.getenv("API_KEY"))

API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

def ask_ai(prompt):
    response = requests.post(
        API_URL,
        headers=headers,
        json={
            "model": "openrouter/auto",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful coding assistant.\n"
                        "Always respond with:\n"
                        "1. A clean code solution\n"
                        "2. A short explanation"
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    )

    # Debug info (can remove later)
    print("\nSTATUS:", response.status_code)

    try:
        return response.json()
    except:
        return {"error": "Invalid JSON response"}


def format_output(result):
    try:
        output = result["choices"][0]["message"]["content"]

        print("\n" + "="*50)
        print("💡 AI RESPONSE")
        print("="*50 + "\n")

        print(output)

        print("\n" + "="*50)

    except:
        print("\n❌ Could not parse response.")
        print("Raw output:", result)


def main():
    print("\n🧠 AI Code Assistant\n")

    mode = input("Choose mode:\n1 = Write Code\n2 = Explain Code\n3 = Fix Code\n\nEnter choice: ")

    user_input = input("\nEnter your request:\n")

    if mode == "1":
        prompt = f"Write code for this request:\n{user_input}"
    elif mode == "2":
        prompt = f"Explain this code clearly:\n{user_input}"
    elif mode == "3":
        prompt = f"Fix bugs in this code and explain:\n{user_input}"
    else:
        prompt = user_input

    result = ask_ai(prompt)
    format_output(result)


if __name__ == "__main__":
    main()
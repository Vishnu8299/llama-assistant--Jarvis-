from flask import Flask, request, jsonify, render_template
import subprocess
import os
from langchain_ollama import OllamaLLM

app = Flask(__name__)

model = OllamaLLM(model="phi3")
history_file = "conversation_history.txt"

def save_history(history):
    with open(history_file, "w", encoding="utf-8") as file:
        file.write("\n".join(history) + "\n")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_text():
    user_input = request.json.get('input', '').strip()

    if user_input:
        print(f"Received user input: {user_input}")

        # Load existing history if available
        conversation_history = []
        if os.path.exists(history_file):
            with open(history_file, "r", encoding="utf-8") as file:
                conversation_history = file.read().splitlines()

        # Update history with user input
        conversation_history.append(f"User: {user_input}")
        prompt = "\n".join(conversation_history) + "\nBot:"

        # Get model response
        result = model.invoke(input=prompt).strip()
        print(f"Model response: {result}")

        # Update history with model response
        conversation_history.append(f"Bot: {result}")

        # Check for command execution
        if "execute" in result.lower():
            command = result.lower().replace("execute", "").strip()
            command_result = subprocess.run(command, shell=True, capture_output=True, text=True)
            result = f"Executed command. Output: {command_result.stdout + command_result.stderr}"

        # Save history
        save_history(conversation_history)
        return jsonify({"response": result})

    return jsonify({"error": "No input provided"}), 400

if __name__ == "__main__":
    app.run(debug=True)

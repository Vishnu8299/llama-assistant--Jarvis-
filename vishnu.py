from flask import Flask, request, jsonify, render_template
import subprocess
import os
import time
from langchain_ollama import OllamaLLM

app = Flask(__name__)
model = OllamaLLM(model="llama3")
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
        # Load existing history if available
        conversation_history = []
        if os.path.exists(history_file):
            with open(history_file, "r", encoding="utf-8") as file:
                conversation_history = file.read().splitlines()

        # Update history with user input
        conversation_history.append(f"User: {user_input}")
        prompt = "\n".join(conversation_history) + "\nBot:"

        try:
            # Measure the start time
            start_time = time.time()
            
            # Get model response
            result = model.invoke(input=prompt).strip()
            
            # Measure the end time
            end_time = time.time()
            
            # Calculate the response time
            response_time = end_time - start_time

            # Update history with model response
            conversation_history.append(f"Bot: {result}")

            # Check for command execution
            if "execute" in result.lower():
                command = result.lower().replace("execute", "").strip()
                command_result = subprocess.run(command, shell=True, capture_output=True, text=True)
                result = f"Executed command. Output: {command_result.stdout + command_result.stderr}"

            # Save history
            save_history(conversation_history)
            
            # Return the response and response time
            return jsonify({"response": result, "response_time": response_time})

        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    return jsonify({"error": "No input provided"}), 400

if __name__ == "__main__":
    app.run(debug=True)

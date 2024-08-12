
import subprocess
import pyttsx3
from langchain_ollama import OllamaLLM
import os
import asyncio

# Initialize the TTS engine
tts_engine = pyttsx3.init()

# Create an instance of the OllamaLLM with the model name
model = OllamaLLM(model="llama3")

# File to store conversation history
history_file = "conversation_history.txt"

# Load conversation history from file
def load_history():
    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as file:
            return file.read().splitlines()
    return []

# Save conversation history to file
def save_history(history):
    with open(history_file, "w", encoding="utf-8") as file:
        for line in history:
            file.write(f"{line}\n")

# Initialize conversation history
conversation_history = load_history()

# Function to speak the output text
def speak_text(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Function to execute system commands
async def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)

# Main processing function
async def process_text(user_input):
    if user_input:
        # Update conversation history with user input
        conversation_history.append(f"User: {user_input}")

        # Combine history into a single prompt
        prompt = "\n".join(conversation_history) + "\nBot:"

        # Invoke the model with the conversation history
        result = model.invoke(input=prompt)
        print(f"Model response: {result}")

        # Update conversation history with model response
        conversation_history.append(f"Bot: {result}")

        # Check if the model's response indicates a command
        if "execute" in result.lower():
            command = result.lower().replace("execute", "").strip()
            command_output = await execute_command(command)
            response = f"Executed command. Output: {command_output}"
        else:
            response = result

        # Convert the result to speech
        speak_text(response)
        
        # Save conversation history to file
        save_history(conversation_history)

# Main function to start processing text input
def main():
    loop = asyncio.get_event_loop()
    while True:
        user_input = input("You: ")
        loop.run_until_complete(process_text(user_input))

if __name__ == "__main__":
    # Run the main function
    main()

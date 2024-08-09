from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import speech_recognition as sr
import pyttsx3

# Define the prompt template
template = """
Answer the question below.
Here is the conversation history: {context}
Question: {question}
Answer:
"""

# Initialize the model
model = OllamaLLM(model="llama3")

# Create a prompt template
prompt = ChatPromptTemplate.from_template(template)

# Combine the prompt and model into a chain
chain = prompt | model

# Initialize the text-to-speech engine
tts_engine = pyttsx3.init()

def get_text_from_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your voice input...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            print("Sorry, there was an issue with the speech recognition service.")
            return ""

def speak_text(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

def load_conversation_history(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return ""

def save_conversation_history(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def handle_conversation():
    file_path = "conversation_history.txt"
    context = load_conversation_history(file_path)
    
    print("Welcome to the AI ChatBot! Type 'exit' to quit.")
    
    # Ask user for input method
    choice = input("Would you like to input text (t) or voice (v)? ").strip().lower()
    
    while True:
        if choice == 'v':
            user_input = get_text_from_voice()
        elif choice == 't':
            user_input = input("You: ")
        else:
            print("Invalid choice, please select 't' for text or 'v' for voice.")
            choice = input("Would you like to input text (t) or voice (v)? ").strip().lower()
            continue
        
        if user_input.lower() == "exit":
            break
        
        result = chain.invoke({"context": context, "question": user_input})
        print("Bot: ", result)
        speak_text(result)
        
        # Update the context and save it
        context += f"\nUser: {user_input}\nAI: {result}"
        save_conversation_history(file_path, context)

if __name__ == "__main__":
    handle_conversation()

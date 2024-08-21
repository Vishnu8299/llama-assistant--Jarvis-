# Jarvis Assistant

Jarvis Assistant is a voice-activated assistant that leverages speech recognition and natural language processing to interact with users and execute system commands. This project integrates various libraries and tools to create an interactive conversational agent.

## Features

- **Speech Recognition**: Captures and converts spoken input to text using Google's speech recognition service.
- **Text-to-Speech**: Converts text responses into spoken output using the `pyttsx3` library.
- **Natural Language Processing**: Uses the OllamaLLM model for generating responses based on conversation history.
- **Command Execution**: Executes system commands based on user requests.
## Requirements

- Python 3.x
- `speech_recognition`
- `pyttsx3`
- `langchain_ollama`
- `subprocess` (standard library)
- `os` (standard library)

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/Vishnu8299/jarvis-assistant.git
    ```
2. Navigate to the project directory:
    ```bash
    cd jarvis-assistant
    ```
3. Install the required Python packages:
    ```bash
    pip install SpeechRecognition pyttsx3 langchain_ollama
    ```

## Usage

1. Run the script:
    ```bash
    python jarvis_assistant.py
    ```
2. Speak into the microphone when prompted. The assistant will process your input, respond, and execute commands if specified.

## Configuration

- **Model Configuration**: The OllamaLLM model is initialized with `llama3`. Adjust the model parameter as needed.

- **Conversation History**: Conversation history is stored in `conversation_history.txt`. This file is updated after each interaction.

## Troubleshooting

- **Speech Recognition Errors**: Ensure your microphone is working and properly configured. Check your internet connection if using an online service.
- **Command Execution Issues**: Ensure that the commands you input are valid and executable on your system.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Author

[Pradeep Ravula](https://github.com/pradeepravula8)
[Vishnu vemula](https://github.com/vishnu8299)

# Python LLM Agent

A powerful LLM agent implementation using LangChain and Ollama with speech recognition capabilities.

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install speech recognition dependencies:
   ```bash
   # For macOS
   brew install portaudio
   pip install pyaudio
   
   # For Ubuntu/Debian
   sudo apt-get install python3-pyaudio
   
   # For Windows
   # Download and install PyAudio wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
   ```

4. Set up Ollama:
   - Install Ollama from https://ollama.ai/
   - Pull the Llama 2 model:
     ```bash
     ollama pull llama2
     ```

## Usage

Run the agent:
```bash
python main.py
```

The agent will start an interactive session where you can:
1. Type your question and press Enter
2. Press Enter to start voice input, speak your question, and press Enter again to stop recording
3. Type 'quit' to exit the session

## Features

- Uses Ollama with Llama 2 model
- Implements a basic agent with tools including:
  - Wikipedia search
  - Web search (configurable)
- Interactive command-line interface with colored output
- Speech recognition for voice input
- Text-to-speech for responses
- Error handling and graceful exit
- Source attribution for responses

## Project Structure

```
.
├── agents/           # Agent implementations
├── tools/           # Tool implementations
├── utils/           # Utility functions
├── models/          # Model storage
├── open-webui/      # Web UI configuration
├── main.py          # Main application entry point
├── text_to_speech.py # Text-to-speech implementation
└── requirements.txt  # Project dependencies
```

## Customization

You can customize the agent by:
1. Adding more tools in the `tools/` directory
2. Modifying the system prompt in the agent implementation
3. Changing the Ollama model parameters
4. Adding more sophisticated error handling
5. Adjusting speech recognition parameters in `utils/speech_recognition_util.py`

## System Requirements

- Python 3.8 or higher
- At least 8GB of RAM (16GB recommended)
- Sufficient disk space for the model
- Working microphone for speech recognition
- Speakers for text-to-speech output
- Ollama installed and running locally

## Web UI

For a web-based interface, you can use Open WebUI:

```bash
docker run -d -p 3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  -e OLLAMA_BASE_URL=http://127.0.0.1:11434 \
  -v ./open-webui:/app/backend/data \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main
```

Access the web interface at http://localhost:3000

## Dependencies

Key dependencies include:
- langchain>=0.1.0
- python-dotenv>=1.0.0
- pydantic>=2.0.0
- langchain-community>=0.0.10
- langchain-ollama>=0.0.1
- wikipedia>=1.4.0
- pyttsx3
- duckduckgo-search
- pyaudio
- SpeechRecognition
- scholarly==1.7.11
- colorama
import threading

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import pyttsx3

class SpeakingCallbackHandler(StreamingStdOutCallbackHandler):
    def __init__(self):
        super().__init__()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 200)
        self.engine.setProperty('volume', 0.9)
        
        # Try to set a female voice if available
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if 'female' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
        self.text_buffer = []
        self.buffer_lock = threading.Lock()
        self.speaking_thread = threading.Thread(target=self._speak_buffer, daemon=True)
        self.speaking_thread.start()
    
    def _speak_buffer(self):
        while True:
            with self.buffer_lock:
                if self.text_buffer:
                    text = ' '.join(self.text_buffer)
                    self.text_buffer.clear()
                else:
                    text = None
            
            # Small sleep to prevent CPU overuse
            threading.Event().wait(0.1)
    
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Run on new token."""
        print(token, end="", flush=True)
        
        # Add token to buffer
        with self.buffer_lock:
            self.text_buffer.append(token)
            
            # If we have a complete sentence or punctuation, speak it
            if any(p in token for p in ['.', '!', '?', '\n']):
                text = ' '.join(self.text_buffer)
                self.text_buffer.clear()
                try:
                    self.engine.say(text)
                    self.engine.runAndWait()
                except Exception as e:
                    print(f"\nSpeech error: {str(e)}")
    
    def on_llm_end(self, *args, **kwargs) -> None:
        """Run on end of LLM."""    

        print('\n\n')
        print('-'*50)
        print('-'*50)
        print('\n\n')

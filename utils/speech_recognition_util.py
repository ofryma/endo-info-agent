import speech_recognition as sr
from speech_recognition import Recognizer, Microphone
import time

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = Recognizer()
        self.microphone = Microphone()
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
    
    def listen_for_input(self, timeout=5, phrase_time_limit=10):
        """
        Listen for speech input and convert it to text.
        
        Args:
            timeout (int): How long to wait for the phrase to start
            phrase_time_limit (int): Maximum time to listen for a phrase
            
        Returns:
            str: The recognized text, or None if no speech was detected
        """
        try:
            print("\nListening... (Press Enter to stop)")
            
            with self.microphone as source:
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
            
            print("Processing speech...")
            text = self.recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            return text
            
        except sr.WaitTimeoutError:
            print("No speech detected within timeout period")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
        except Exception as e:
            print(f"Error during speech recognition: {e}")
            return None 

if __name__ == "__main__":
    print("Speech Recognition Demo")
    print("======================")
    print("This program will listen for your voice and convert it to text.")
    print("Press Ctrl+C to exit the program.")
    
    recognizer = SpeechRecognizer()
    
    try:
        while True:
            print("\nSpeak now...")
            text = recognizer.listen_for_input()
            if text:
                print(f"You said: {text}")
            time.sleep(1)  # Small pause between listening sessions
            
    except KeyboardInterrupt:
        print("\nExiting program...") 
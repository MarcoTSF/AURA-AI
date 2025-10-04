import pyttsx3
import speech_recognition as sr
from dotenv import load_dotenv

load_dotenv()

# Engine de voz
engine = pyttsx3.init()
engine.setProperty("rate", 180)

# Reconhecimento de voz
recognizer = sr.Recognizer()
microfone = sr.Microphone()
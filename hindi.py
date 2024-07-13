from translate import Translator
from gtts import gTTS
import pygame
from langdetect import detect
import os

def translate_text(text, target_language='en'):
    try:
        translator = Translator(from_lang=detect_language(text), to_lang=target_language)
        translation = translator.translate(text)
        return translation
    except Exception as e:
        print(f"Error during translation: {e}")
        return ""

def text_to_speech(text, lang='en'):
    assert text, "No text to speak"
    try:
        tts = gTTS(text=text, lang=lang)
        
        # Ensure any existing output.mp3 file is removed before saving the new one
        if os.path.exists("output.mp3"):
            os.remove("output.mp3")
        
        tts.save("output.mp3")
        
        # Initialize the mixer
        pygame.mixer.init()
        # Load the mp3 file
        pygame.mixer.music.load("output.mp3")
        # Play the mp3 file
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():  # Wait for the music to finish playing
            pygame.time.Clock().tick(10)
        pygame.mixer.music.unload()  # Explicitly unload the music
        pygame.mixer.quit()  # Ensure the mixer is properly closed
    except Exception as e:
        print(f"Error during text-to-speech conversion: {e}")

def detect_language(text):
    try: 
        return detect(text)
    except Exception as e:
        print(f"Error during language detection: {e}")
        return 'en'

def multilingual_text_to_speech(text, target_language='es'):
    source_language = detect_language(text)
    print(f"Detected source language: {source_language}")
    
    translated_text = translate_text(text, target_language)
    print(f"Translated text: {translated_text}")

    # Check if the translated text is empty
    if not translated_text.strip():
        print("Translation failed or returned empty text.")
        return

    text_to_speech(translated_text, target_language)

# Test case to verify Hindi translation and TTS
test_text = "Hello everyone"
target_language = 'hi'

print(f"Original text: {test_text}")
multilingual_text_to_speech(test_text, target_language)

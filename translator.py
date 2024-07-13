'''from translate import Translator
from gtts import gTTS
from playsound import playsound
from langdetect import detect
import os

def translate_text(text, target_language='en'):
    translator = Translator(from_lang=detect_language(text), to_lang=target_language)
    translation = translator.translate(text)
    return translation

def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    
    tts.save("output.mp3")
    playsound("output.mp3")

def detect_language(text):
    try: 
        return detect(text)
    except:
        return 'en'

    

def multilingual_text_to_speech(text, target_language='en'):
    source_language = detect_language(text)
    print(f"Detected source language: {source_language}")
    
    translated_text = translate_text(text, target_language)
    print(f"Translated text: {translated_text}")
    
    text_to_speech(translated_text, target_language)

# Example usage
#text = "how are you"
#target_language = 'es'  # Translate to English

#multilingual_text_to_speech(text, target_language)'''
import tkinter as tk
from tkinter import ttk
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

    # Check if the target language is Hindi and if the translation was successful
    if target_language == 'hi':
        if translated_text.strip() == "":
            print("Translation to Hindi failed.")
            return
        else:
            print(f"Translated text to Hindi: {translated_text}")

    text_to_speech(translated_text, target_language)

def read_data_from_file(filename):
    try:
        # Open the file in read mode
        with open(filename, 'r') as file:
            # Read the content of the file
            data = file.read()
        return data
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None

def open_file():
    # file_path = filedialog.askopenfilename()
    file_path = 'transl.txt'
    if file_path:
        text = read_data_from_file(file_path)
        return text
    return None

def on_convert_button_click():
    selected_language = language_combobox.get()
    text = open_file()
    if text:
        multilingual_text_to_speech(text, selected_language)

# Set up the main application window
root = tk.Tk()
root.title("Multilingual Text to Speech")

# Create and place the label
label = ttk.Label(root, text="Select Destination Language:")
label.pack(pady=10)

# Create and place the combobox
language_combobox = ttk.Combobox(root, values=['en', 'es', 'fr', 'hi', 'te'])
language_combobox.pack(pady=10)
language_combobox.set('en')  # Set default value

# Create and place the button
convert_button = ttk.Button(root, text="Convert", command=on_convert_button_click)
convert_button.pack(pady=20)

# Run the application
root.mainloop()

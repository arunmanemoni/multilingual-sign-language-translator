import tkinter as tk
from tkinter import ttk
from translate import Translator
import pyttsx3
import pygame
from langdetect import detect
import os

# Mapping from ISO 639-1 language codes to human-readable names
LANGUAGE_CODES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'hi': 'Hindi',
    'te': 'Telugu',
    'zh': 'Chinese',
    'de': 'German',
    'ja': 'Japanese',
    'ko': 'Korean',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'it': 'Italian'
}

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
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)    # Speed percent (can go over 100)
        engine.setProperty('volume', 0.9)  # Volume 0-1
        
        # Language code mapping for pyttsx3
        language_mapping = {
            'en': 'english',
            'es': 'spanish',
            'fr': 'french',
            'hi': 'hindi',
            'te': 'te',   # Assuming 'te' is Telugu, adjust if needed
            'zh': 'chinese',
            'de': 'german',
            'ja': 'japanese',
            'ko': 'korean',
            'pt': 'portuguese',
            'ru': 'russian',
            'it': 'italian'
        }
        
        engine.setProperty('voice', language_mapping.get(lang, 'english'))
        engine.say(text)
        engine.runAndWait()
        engine.stop()
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
    selected_language_code = language_combobox.get()
    selected_language = LANGUAGE_CODES.get(selected_language_code, 'en')
    text = open_file()
    if text:
        multilingual_text_to_speech(text, selected_language_code)

# Set up the main application window
root = tk.Tk()
root.title("Multilingual Text to Speech")

# Create and place the label
label = ttk.Label(root, text="Select Destination Language:")
label.pack(pady=10)

# Create and place the combobox
language_combobox = ttk.Combobox(root, values=list(LANGUAGE_CODES.values()))
language_combobox.pack(pady=10)
language_combobox.set('English')  # Set default value

# Create and place the button
convert_button = ttk.Button(root, text="Convert", command=on_convert_button_click)
convert_button.pack(pady=20)

# Run the application
root.mainloop()

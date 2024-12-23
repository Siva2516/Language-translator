# Import libraries
import speech_recognition as sr
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import pygame
import tempfile
import os
from pathlib import Path
from time import sleep

# Map googletrans language codes to gTTS supported codes
language_name_to_code = {
    "Afrikaans": "af", "Arabic": "ar", "Bengali": "bn", "Chinese (Simplified)": "zh-cn", "Czech": "cs",
    "Danish": "da", "Dutch": "nl", "English": "en", "Finnish": "fi", "French": "fr",
    "German": "de", "Greek": "el", "Gujarati": "gu", "Hindi": "hi", "Hungarian": "hu",
    "Indonesian": "id", "Italian": "it", "Japanese": "ja", "Kannada": "kn", "Korean": "ko",
    "Malayalam": "ml", "Marathi": "mr", "Nepali": "ne", "Norwegian": "no", "Polish": "pl",
    "Portuguese": "pt", "Punjabi": "pa", "Romanian": "ro", "Russian": "ru", "Spanish": "es",
    "Swedish": "sv", "Tamil": "ta", "Telugu": "te", "Thai": "th", "Turkish": "tr",
    "Ukrainian": "uk", "Urdu": "ur", "Vietnamese": "vi"
}

# Function to display supported languages
def display_languages():
    print("Supported Languages:")
    for language in language_name_to_code:
        print(language)

# Function for Speech-to-Speech Translation
def speech_to_speech_translation():
    # Initialize recognizer and translator
    recognizer = sr.Recognizer()
    translator = Translator()

    # Display supported languages
    display_languages()
    target_language_name = input("\nEnter the target language (e.g., 'Spanish', 'Telugu'): ").strip().title()

    # Check if the language name is valid
    if target_language_name not in language_name_to_code:
        print("Invalid language. Please try again.")
        return

    # Get the language code from the dictionary
    target_language_code = language_name_to_code[target_language_name]
    print(f"Using language code: {target_language_code}")

    print("\n🎙 Speak now...")

    try:
        # Capture speech input
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
            print("Listening...")
            audio_data = recognizer.listen(source)

        # Recognize speech
        print("\n🔍 Recognizing speech...")
        recognized_text = recognizer.recognize_google(audio_data)
        print(f"🗣 Original Speech: {recognized_text}")

        # Translate text
        print("\n🌍 Translating...")
        translated_text = translator.translate(recognized_text, dest=target_language_code).text
        print(f"📝 Translated Text: {translated_text}")

        # Convert translated text to speech
        print("\n🔊 Converting to speech...")
        tts = gTTS(text=translated_text, lang=target_language_code)

        # Use a simple path to avoid issues
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)
        temp_file_path = temp_file.name

        # Play the speech using pygame
        print("🎧 Playing the translated speech...")
        pygame.mixer.init()
        pygame.mixer.music.load(temp_file_path)
        pygame.mixer.music.play()

        # Wait for the music to finish before continuing
        while pygame.mixer.music.get_busy():
            sleep(1)

        print("✅ Speech finished playing.")

    except sr.UnknownValueError:
        print("❌ Sorry, I could not understand your speech.")
    except sr.RequestError as e:
        print(f"❌ Speech recognition service error: {e}")
    except Exception as ex:
        print(f" {ex}")
    finally:
        # Ensure the file is not in use before removing
        if 'temp_file_path' in locals():
            try:
                # Check if the file exists before removing it
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
                    print("✅ Temporary file removed.")
                else:
                    print(f"❌ File not found: {temp_file_path}")
            except PermissionError:
                print(f"{temp_file_path}")

# Run the translator function
print("🎙 Welcome to the Speech-to-Speech Translator 🎙")
speech_to_speech_translation()
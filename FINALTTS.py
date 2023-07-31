import pyaudio
import queue
import threading
from pynput import keyboard

from google.cloud import texttospeech

# Function to synthesize speech from the input string of text
# (same as before)
def synthesize_text(text):
    """Synthesizes speech from the input string of text."""
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-C",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    return response.audio_content
def synthesize_and_play(word):
    audio_data = synthesize_text(word)
    stream.write(audio_data)

def on_key_press(key):
    global current_word

    try:
        char = key.char
        if char == " ":
            if current_word:
                # print("Current WordHI:", current_word)
                # synthesize_and_play(current_word)
                current_word = ""
        else:
            current_word += char
    except AttributeError:
        if key == keyboard.Key.space:
            if current_word:
                # print("Current Word:", current_word)
                synthesize_and_play(current_word)
                current_word = ""

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(2),
                channels=1,
                rate=22050,
                output=True)
current_word = ""

print("Listener started. Type each word and press 'Space' after each word to hear it spoken.")

# Create a listener for key presses
with keyboard.Listener(on_press=on_key_press) as listener:
    listener.join()

stream.stop_stream()
stream.close()
p.terminate()

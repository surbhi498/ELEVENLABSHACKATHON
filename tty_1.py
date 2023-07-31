import speech_recognition as sr

def speech_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak something...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
        audio = recognizer.listen(source, timeout=5)  # Set timeout to 5 seconds

    try:
        # Use the Google Web Speech API to perform speech recognition
        text = recognizer.recognize_google(audio)
        print(f"Text: {text}")
        return text
    except sr.UnknownValueError:
        print("Speech recognition could not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech API; {e}")
        return None

if __name__ == "__main__":
    print("Real-time Speech-to-Text. Say something and see the text output.")
    while True:
        text = speech_to_text()
        if not text:
            print("No speech detected. Stopping input.")
            break
        if text.lower() == 'exit':
            break

import os
from dotenv import load_dotenv
import threading
import time
#from eleven_tts import ElevenTTS
import pyaudio
import concurrent.futures
# Load variables from .env file into the environment
load_dotenv()
from google.cloud import speech_v1p1beta1 as speech
api_key = os.getenv('API_KEY')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/surbhisharma/Documents/TWOWAYCHATAUDIOSYSTEM/api.json'
#tts_engine = ElevenTTS(api_key=api_key)
# Set up Google Cloud Speech-to-Text client
client = speech.SpeechClient()

# def process_response(response):
#     # Process the API response to extract partial or final transcriptions
#     last_transcript = ""
#     for result in response.results:
#         if result.alternatives:
#             transcript = result.alternatives[0].transcript
#             if transcript != last_transcript:
#                 #print(transcript)
#                 # is_final = result.is_final
#                 # print(f"{'Final' if is_final else 'Partial'}: {transcript}")
#                 update_chat_interface(transcript)
#                 last_transcript = transcript
#             #print(transcript)
#             # is_final = result.is_final
#             # print(f"{'Final' if is_final else 'Partial'}: {transcript}")
#             #update_chat_interface(transcript)

# def audio_stream():
#     # Constants for audio stream configuration
#     chunk_size = 1024
#     sample_rate = 16000

#     # Set up PyAudio
#     audio = pyaudio.PyAudio()
#     stream = audio.open(format=pyaudio.paInt16,
#                         channels=1,
#                         rate=sample_rate,
#                         input=True,
#                         frames_per_buffer=chunk_size)

#     print("Listening...")
#     # Create a thread for audio streaming
#     # audio_thread = threading.Thread(target=stream_audio, args=(audio, stream, chunk_size, streaming_config))
#     # audio_thread.start()

#     # # Set a timer for 5 seconds
#     # timeout = 5
#     # start_time = time.time()

#     # while audio_thread.is_alive():
#     #     if time.time() - start_time >= timeout:
#     #         print("Timeout reached. Stopping audio stream.")
#     #         stream.stop_stream()
#     #         stream.close()
#     #         audio.terminate()
#     #         break

#     # audio_thread.join()
#     # Start streaming audio to Google Cloud Speech-to-Text API
#     streaming_config = speech.StreamingRecognitionConfig(
#         config=speech.RecognitionConfig(
#             encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#             sample_rate_hertz=sample_rate,
#             language_code="en-US",  # Update with your desired language code
#         ),
#         interim_results=True  # Get partial transcriptions as well
#     )

#     requests = (
#         speech.StreamingRecognizeRequest(audio_content=stream.read(chunk_size))
#         for _ in range(100000)  # Adjust the number of iterations based on your use case
#     )

#     responses = client.streaming_recognize(config=streaming_config, requests=requests)

#     # Process API responses in real-time
#     for response in responses:
#         process_response(response)

#     # Stop the audio stream
#     stream.stop_stream()
#     stream.close()
#     audio.terminate()

# def update_chat_interface(text):
#     # Clear the line and print the recognized text
#     print("\r" + text, end="")

# def stt_function(timeout=5):
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         # Execute the audio_stream function in a separate thread
#         future = executor.submit(audio_stream)

#         try:
#             # Wait for the function to complete with a timeout
#             result = future.result(timeout=timeout)
#         except concurrent.futures.TimeoutError:
#             print("\nTimeout: Speech recording ended.")
#             return

import concurrent.futures
import streamlit as st
import pyaudio

def audio_stream(callback):
    # Constants for audio stream configuration
    chunk_size = 1024
    sample_rate = 16000

    # Set up PyAudio
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk_size)

    print("Listening...")

    # Start streaming audio to Google Cloud Speech-to-Text API
    streaming_config = speech.StreamingRecognitionConfig(
        config=speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=sample_rate,
            language_code="en-US",  # Update with your desired language code
        ),
        interim_results=True  # Get partial transcriptions as well
    )

    # Create a list to store audio chunks
    audio_chunks = []

    # Set a flag to indicate recording is in progress
    # recording_started = True
    is_recording = True

    try:
        while is_recording:
            audio_chunk = stream.read(chunk_size)
            audio_chunks.append(audio_chunk)

            # When the button is clicked, stop recording and initiate speech-to-text
            if not is_recording:
                break

            # Check if the callback function is provided and call it with the current audio chunk
            if callback:
                callback(audio_chunk)
    except Exception as e:
        print("Error during recording:", e)
    finally:
        # Stop the audio stream and clean up
        stream.stop_stream()
        stream.close()
        audio.terminate() 
    

    # Combine audio chunks and perform speech-to-text
    audio_content = b''.join(audio_chunks)
    requests = [speech.StreamingRecognizeRequest(audio_content=audio_content)]
    response = client.streaming_recognize(config=streaming_config, requests=requests)

    # Call the callback function with the final response
    if callback and response.results:
        callback(response.results)








       

# def stt_function(timeout=5):
#     # Create a button to start recording
#     if st.button("Start Recording"):
#         # Use ThreadPoolExecutor to run the audio_stream function in a separate thread
#         with concurrent.futures.ThreadPoolExecutor() as executor:
#             # Execute the audio_stream function in a separate thread
#             future = executor.submit(audio_stream, callback=None)  # We don't need a callback here

#             try:
#                 # Wait for the function to complete with a timeout
#                 result = future.result(timeout=timeout)
#             except concurrent.futures.TimeoutError:
#                 print("\nTimeout: Speech recording ended.")
#                 return
# is_recording = False
# def stt_function(timeout=5):
#     # Flag to prevent concurrent calls to stt_function
#     global is_recording

#     # Ensure that the function is not called again while it's already running
#     if is_recording:
#         st.warning("Speech recording is already in progress. Please wait for the current recording to finish.")
#         return

#     # Create a button to start recording
#     if st.button("Start Recording"):
#         # Set the flag to indicate recording is in progress
#         is_recording = True

#         # Use ThreadPoolExecutor to run the audio_stream function in a separate thread
#         with concurrent.futures.ThreadPoolExecutor() as executor:
#             # Execute the audio_stream function in a separate thread
#             future = executor.submit(audio_stream, callback=None)  # We don't need a callback here

#             try:
#                 # Wait for the function to complete with a timeout
#                 result = future.result(timeout=timeout)
#             except concurrent.futures.TimeoutError:
#                 print("\nTimeout: Speech recording ended.")
#                 st.error("Timeout: Speech recording ended.")
#             finally:
#                 # Reset the flag after the recording is done
#                 global is_recording
#                 is_recording = False

# Rest of your code...

# if __name__ == "__main__":
#     main()






# Rest of your code...

# if __name__ == "__main__":
#     main()

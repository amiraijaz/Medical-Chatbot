# voice_of_the_patient.py
from dotenv import load_dotenv
load_dotenv()

import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import os
from groq import Groq

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    """
    Simplified function to record audio from the microphone and save it as an MP3 file.
    """
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")
            
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")
            
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")
            
            logging.info(f"Audio saved to {file_path}")
            return True
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return False

def transcribe_with_groq(audio_filepath, stt_model="whisper-large-v3"):
    """
    Transcribe audio using Groq's Whisper model.
    """
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set in environment variables")
    
    client = Groq(api_key=GROQ_API_KEY)
    
    try:
        with open(audio_filepath, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=stt_model,
                file=audio_file,
                language="en"
            )
        return transcription.text
    except Exception as e:
        logging.error(f"Transcription failed: {e}")
        return ""

# For testing
if __name__ == "__main__":
    audio_filepath = "patient_voice_test_for_patient.mp3"
    record_audio(file_path=audio_filepath)
    if os.path.exists(audio_filepath):
        transcription = transcribe_with_groq(audio_filepath)
        print("Transcription:", transcription)
    else:
        print(f"Audio file {audio_filepath} not found")
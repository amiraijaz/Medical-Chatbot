# voice_of_the_doctor.py
from dotenv import load_dotenv
load_dotenv()

import os
from gtts import gTTS
import subprocess
import platform
from elevenlabs.client import ElevenLabs
import elevenlabs

def text_to_speech_with_gtts(input_text, output_filepath):
    """
    Convert text to speech using gTTS and play it.
    """
    language = "en"
    try:
        audioobj = gTTS(text=input_text, lang=language, slow=False)
        audioobj.save(output_filepath)
        
        os_name = platform.system()
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath], check=True)
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'], check=True)
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath], check=True)
        else:
            raise OSError("Unsupported operating system")
        return output_filepath
    except Exception as e:
        print(f"An error occurred while generating/playing gTTS audio: {e}")
        return None

def text_to_speech_with_elevenlabs(input_text, output_filepath):
    """
    Convert text to speech using ElevenLabs and play it.
    """
    ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
    if not ELEVENLABS_API_KEY:
        print("ELEVENLABS_API_KEY not set, falling back to gTTS")
        return text_to_speech_with_gtts(input_text, output_filepath)
    
    try:
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        audio = client.generate(
            text=input_text,
            voice="Aria",
            output_format="mp3_22050_32",
            model="eleven_turbo_v2"
        )
        elevenlabs.save(audio, output_filepath)
        
        os_name = platform.system()
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath], check=True)
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'], check=True)
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath], check=True)
        else:
            raise OSError("Unsupported operating system")
        return output_filepath
    except Exception as e:
        print(f"An error occurred while generating/playing ElevenLabs audio: {e}")
        return None

# For testing
if __name__ == "__main__":
    input_text = "Hi, this is AI with Hassan, autoplay testing!"
    text_to_speech_with_elevenlabs(input_text, "elevenlabs_testing_autoplay.mp3")
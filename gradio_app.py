# gradio_app.py
from dotenv import load_dotenv
load_dotenv()

import os
import gradio as gr
from voice_of_the_patient import record_audio, transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_elevenlabs
from brain_of_the_doctor import encode_image, analyze_image_with_query

system_prompt = """You have to act as a professional doctor, i know you are not but this is for learning purpose. 
What's in this image?. Do you find anything wrong with it medically? 
If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
Donot say 'In the image I see' but say 'With what I see, I think you have ....'
Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

def process_inputs(audio_filepath, image_filepath):
    """
    Process audio and image inputs to generate a doctor's response.
    """
    try:
        # Transcribe audio
        speech_to_text_output = transcribe_with_groq(audio_filepath=audio_filepath)
        if not speech_to_text_output:
            return "Failed to transcribe audio", "", None

        # Analyze image with transcription
        doctor_response = "No image provided for me to analyze"
        if image_filepath and os.path.exists(image_filepath):
            encoded_image = encode_image(image_filepath)
            if encoded_image:
                doctor_response = analyze_image_with_query(
                    query=system_prompt + speech_to_text_output,
                    encoded_image=encoded_image,
                    model="llama-3.3-70b-versatile"
                )
            else:
                doctor_response = "Failed to encode image"

        # Convert response to speech
        audio_output = text_to_speech_with_elevenlabs(
            input_text=doctor_response,
            output_filepath="final_doctor_response.mp3"
        )

        return speech_to_text_output, doctor_response, audio_output
    except Exception as e:
        return f"Error processing inputs: {e}", "", None

# Create the Gradio interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath", label="Record Your Symptoms"),
        gr.Image(type="filepath", label="Upload Medical Image (Optional)")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text Output"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio(label="Doctor's Audio Response")
    ],
    title="AI Doctor with Vision and Voice",
    description="Record your symptoms and optionally upload an image for a simulated doctor response."
)

if __name__ == "__main__":
    iface.launch(debug=False, server_name="127.0.0.1", server_port=7860)
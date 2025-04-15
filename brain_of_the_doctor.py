# brain_of_the_doctor.py
from dotenv import load_dotenv
load_dotenv()

import os
import base64
from groq import Groq

# Step 1: Setup GROQ API key
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in environment variables")

# Step 2: Convert image to required format
def encode_image(image_path):
    """
    Convert an image file to base64 encoding.
    """
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None

# Step 3: Setup Multimodal LLM
def analyze_image_with_query(query, encoded_image, model="llama-3.3-70b-versatile"):
    client = Groq(api_key=GROQ_API_KEY)
    try:
        # Reduce image size if needed (example using PIL)
        from PIL import Image
        import io
        import base64

        # Decode, resize, and re-encode the image
        img_data = base64.b64decode(encoded_image)
        img = Image.open(io.BytesIO(img_data))
        img = img.resize((512, 512))  # Resize to reduce tokens
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG", quality=70)  # Lower quality to reduce size
        encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

        messages = [
            {
                "role": "user",
                "content": f"{query}\n![image](data:image/jpeg;base64,{encoded_image})"
            }
        ]
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model,
            max_tokens=300,  # Reduce max_tokens to stay under limit
            temperature=0.7
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error analyzing image: {e}"

# For testing
if __name__ == "__main__":
    image_path = "acne.jpg"
    query = "Is there something wrong with my face?"
    if os.path.exists(image_path):
        encoded_image = encode_image(image_path)
        if encoded_image:
            response = analyze_image_with_query(query, encoded_image)
            print("Response:", response)
        else:
            print("Failed to encode image")
    else:
        print(f"Image file {image_path} not found")
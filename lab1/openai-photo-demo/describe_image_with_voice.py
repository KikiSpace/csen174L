import base64
import os
from pathlib import Path

from dotenv import load_dotenv
from elevenlabs import save
from elevenlabs.client import ElevenLabs
from openai import OpenAI


PROMPT = (
    "Describe this image in 3-4 clear, friendly sentences for a classroom demo. "
    "Focus on the main objects, the setting, and anything visually notable. "
    "Make it sound natural when read aloud."
)


def main() -> None:
    # 1) Load API keys from .env
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

    # 2) Basic checks for required keys
    if not openai_api_key:
        print("Error: OPENAI_API_KEY is missing in your .env file.")
        return
    if not elevenlabs_api_key:
        print("Error: ELEVENLABS_API_KEY is missing in your .env file.")
        return

    # 3) Check that photo.jpg exists in this folder
    image_path = Path("photo.jpg")
    if not image_path.exists():
        print("Error: photo.jpg was not found in this folder.")
        return

    # 4) Read image bytes and encode as base64 for OpenAI vision input
    with image_path.open("rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

    try:
        # 5) Ask OpenAI to describe the image
        openai_client = OpenAI(api_key=openai_api_key)
        response = openai_client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": PROMPT},
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{image_base64}",
                        },
                    ],
                }
            ],
        )
        description = response.output_text.strip()
    except Exception as error:
        print(f"Error: OpenAI request failed: {error}")
        return

    # 6) Print description for students to see in terminal
    print("\nImage description:\n")
    print(description)

    try:
        # 7) Convert description text to speech with ElevenLabs
        elevenlabs_client = ElevenLabs(api_key=elevenlabs_api_key)
        audio = elevenlabs_client.text_to_speech.convert(
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2",
            text=description,
        )

        # 8) Save audio to output.mp3
        save(audio, "output.mp3")
    except Exception as error:
        print(f"Error: ElevenLabs request failed: {error}")
        return

    print("\nSaved audio to output.mp3")


if __name__ == "__main__":
    main()

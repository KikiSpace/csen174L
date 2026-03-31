import os
import subprocess
from pathlib import Path

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

MODEL_ID = "openai/whisper-large-v3-turbo"


def main() -> None:
    # 1) Load environment variables from .env
    load_dotenv()
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        print("Error: HF_TOKEN is missing in your .env file.")
        return

    # 2) Check that demo.mp4 exists in this folder
    video_path = Path("demo.mp4")
    if not video_path.exists():
        print("Error: demo.mp4 was not found in this folder.")
        return

    # 3) Extract audio from demo.mp4 and save as demo_audio.wav
    audio_path = Path("demo_audio.wav")
    ffmpeg_command = [
        "ffmpeg",
        "-y",
        "-i",
        str(video_path),
        "-vn",
        "-acodec",
        "pcm_s16le",
        "-ar",
        "16000",
        "-ac",
        "1",
        str(audio_path),
    ]

    try:
        subprocess.run(ffmpeg_command, check=True, capture_output=True, text=True)
    except FileNotFoundError:
        print("Error: ffmpeg is not installed or not in your PATH.")
        return
    except subprocess.CalledProcessError as error:
        print("Error: Failed to extract audio from demo.mp4.")
        print(error.stderr.strip())
        return

    # 4) Send audio to Hugging Face ASR and get transcript
    try:
        client = InferenceClient(token=hf_token)
        # Pass the Path object so the SDK can detect the audio/wav MIME type.
        result = client.automatic_speech_recognition(
            audio=audio_path,
            model=MODEL_ID,
        )
    except Exception as error:
        print("Error: Hugging Face ASR request failed.")
        print("The selected model/provider may be unavailable for your account right now.")
        print(f"Details: {error}")
        return

    # 5) Handle response shape safely (string or dictionary-like)
    if isinstance(result, str):
        transcript = result.strip()
    elif isinstance(result, dict):
        transcript = str(result.get("text", "")).strip()
    else:
        transcript = str(getattr(result, "text", "")).strip()

    if not transcript:
        print("Error: Transcription returned empty text.")
        return

    # 6) Print transcript and save to transcript.txt
    print("\nTranscript:\n")
    print(transcript)

    output_file = Path("transcript.txt")
    output_file.write_text(transcript + "\n", encoding="utf-8")
    print("\nSaved transcript to transcript.txt")


if __name__ == "__main__":
    main()

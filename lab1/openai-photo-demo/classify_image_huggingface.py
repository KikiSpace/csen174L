import os
from pathlib import Path

from dotenv import load_dotenv
from huggingface_hub import InferenceClient


CANDIDATE_LABELS = [
    "classroom",
    "desk",
    "technology",
    "campus",
    "food",
    "study space",
]


def main() -> None:
    # 1) Load HF token from .env
    load_dotenv()
    hf_token = os.getenv("HF_TOKEN_READ")
    if not hf_token:
        print("Error: HF_TOKEN is missing in your .env file.")
        return

    # 2) Check that photo.jpg exists
    image_path = Path("photo.jpg")
    if not image_path.exists():
        print("Error: photo.jpg was not found in this folder.")
        return

    # 3) Read the local image
    image_bytes = image_path.read_bytes()

    # 4) Run zero-shot image classification with Hugging Face
    try:
        client = InferenceClient(token=hf_token)
        results = client.zero_shot_image_classification(
            image=image_bytes,
            candidate_labels=CANDIDATE_LABELS,
            model="openai/clip-vit-base-patch32",
        )
    except Exception as error:
        print("Error: Hugging Face request failed.")
        print("The model may be unavailable or your token may not have access.")
        print(f"Details: {error}")
        return

    # 5) Print ranked labels and confidence scores
    print("\nZero-shot image classification results:\n")
    for item in results:
        label = item.label
        score = item.score
        print(f"- {label}: {score:.4f}")


if __name__ == "__main__":
    main()

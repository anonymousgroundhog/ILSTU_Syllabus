"""Example 2: send a PNG image to the Sushi AI Server and print the reply.

The image is base64-encoded and sent inline as a data URL (OpenAI-style
"image_url" content part). Use a vision-capable model such as
llama3.2-vision:latest, gemma3:latest, or qwen3-vl:235b; text-only models
like llama3.1:latest cannot see images.

Usage:
    python send_image.py
    python send_image.py path/to/screenshot.png "What error is shown?"
"""

import argparse
import base64
import sys
from pathlib import Path

from sushi_common import chat, get_api_key

HERE = Path(__file__).parent
VISION_MODEL = "llama3.2-vision:latest"


def main():
    parser = argparse.ArgumentParser(description="Send a PNG image to the Sushi AI Server.")
    parser.add_argument("image", nargs="?", default=str(HERE / "example_files" / "sample_image.png"))
    parser.add_argument("prompt", nargs="?", default="Describe this image. What text does it contain?")
    parser.add_argument("--model", default=VISION_MODEL)
    args = parser.parse_args()

    image_path = Path(args.image)
    if not image_path.is_file():
        sys.exit(f"Image not found: {image_path}")

    b64 = base64.b64encode(image_path.read_bytes()).decode("ascii")
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": args.prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
            ],
        }
    ]

    api_key = get_api_key()
    print(f"> [{image_path.name}] {args.prompt}\n")
    print(chat(api_key, messages, model=args.model))


if __name__ == "__main__":
    main()

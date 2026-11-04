"""Example 3: send a text file to the Sushi AI Server and print the reply.

Two methods are shown:

  inline (default) - read the file and put its contents in the prompt.
                     Simple, and the model sees the whole file.
  upload           - upload the file to Open WebUI (POST /api/v1/files/)
                     and attach it to the chat by its file id. The server
                     indexes the file and gives the model relevant chunks.

Usage:
    python send_text_file.py
    python send_text_file.py path/to/notes.txt "Summarize this."
    python send_text_file.py --method upload
"""

import argparse
import sys
from pathlib import Path

import requests

from sushi_common import BASE_URL, DEFAULT_MODEL, TIMEOUT, auth_headers, chat, get_api_key

HERE = Path(__file__).parent


def ask_inline(api_key, path: Path, prompt: str, model: str) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    content = f"{prompt}\n\n--- BEGIN FILE: {path.name} ---\n{text}\n--- END FILE ---"
    return chat(api_key, [{"role": "user", "content": content}], model=model)


def upload_file(api_key, path: Path) -> str:
    """Upload a file to Open WebUI and return its file id."""
    with path.open("rb") as fh:
        resp = requests.post(
            f"{BASE_URL}/api/v1/files/",
            headers={**auth_headers(api_key), "Accept": "application/json"},
            files={"file": (path.name, fh, "text/plain")},
            timeout=TIMEOUT,
        )
    if resp.status_code != 200:
        sys.exit(f"Upload failed ({resp.status_code}): {resp.text}")
    return resp.json()["id"]


def ask_upload(api_key, path: Path, prompt: str, model: str) -> str:
    file_id = upload_file(api_key, path)
    print(f"(uploaded {path.name} as file id {file_id})\n")
    return chat(
        api_key,
        [{"role": "user", "content": prompt}],
        model=model,
        files=[{"type": "file", "id": file_id}],
    )


def main():
    parser = argparse.ArgumentParser(description="Send a text file to the Sushi AI Server.")
    parser.add_argument("file", nargs="?", default=str(HERE / "example_files" / "sample_log.txt"))
    parser.add_argument(
        "prompt",
        nargs="?",
        default="Summarize this log. List any suspicious events with their timestamps.",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--method", choices=["inline", "upload"], default="inline")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.is_file():
        sys.exit(f"File not found: {path}")

    api_key = get_api_key()
    print(f"> [{path.name}] {args.prompt}\n")
    if args.method == "upload":
        print(ask_upload(api_key, path, args.prompt, args.model))
    else:
        print(ask_inline(api_key, path, args.prompt, args.model))


if __name__ == "__main__":
    main()

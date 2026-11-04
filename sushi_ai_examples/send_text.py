"""Example 1: send a text prompt to the Sushi AI Server and print the reply.

Usage:
    python send_text.py
    python send_text.py "Explain file carving in two sentences."
    python send_text.py "Hello" --model qwen3:latest
"""

import argparse

from sushi_common import DEFAULT_MODEL, chat, get_api_key


def main():
    parser = argparse.ArgumentParser(description="Send a text prompt to the Sushi AI Server.")
    parser.add_argument("prompt", nargs="?", default="In one sentence, what is digital forensics?")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    args = parser.parse_args()

    api_key = get_api_key()
    messages = [{"role": "user", "content": args.prompt}]

    print(f"> {args.prompt}\n")
    print(chat(api_key, messages, model=args.model))


if __name__ == "__main__":
    main()

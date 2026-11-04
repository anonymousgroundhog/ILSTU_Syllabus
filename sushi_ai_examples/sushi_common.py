"""Shared helpers for the Sushi AI Server (Open WebUI) examples.

The server must be reached from inside the ISU network (use the VPN if off campus).
"""

import os
import sys

import requests

BASE_URL = "http://sushi.it.ilstu.edu:8080"
DEFAULT_MODEL = "llama3.1:latest"
TIMEOUT = 300  # seconds; large models can take a while to answer


def get_api_key() -> str:
    """Return the API key from the SUSHI_API_KEY env var, or prompt for it.

    Never hard-code your key in a script you share or commit.
    """
    key = os.environ.get("SUSHI_API_KEY", "").strip()
    if not key:
        key = input("Enter your Sushi API key (Settings -> Account -> API Keys): ").strip()
    if not key:
        sys.exit("An API key is required.")
    return key


def auth_headers(api_key: str) -> dict:
    return {"Authorization": f"Bearer {api_key}"}


def chat(api_key: str, messages: list, model: str = DEFAULT_MODEL, **extra) -> str:
    """Send messages to /api/chat/completions and return the reply text."""
    payload = {"model": model, "messages": messages, **extra}
    resp = requests.post(
        f"{BASE_URL}/api/chat/completions",
        headers=auth_headers(api_key),
        json=payload,
        timeout=TIMEOUT,
    )
    if resp.status_code != 200:
        sys.exit(f"Request failed ({resp.status_code}): {resp.text}")
    return resp.json()["choices"][0]["message"]["content"]

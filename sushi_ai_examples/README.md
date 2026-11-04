# Sushi AI Server – Python Examples

Python examples for the ILSTU Sushi AI Server (Open WebUI) at
`http://sushi.it.ilstu.edu:8080`. You must be on the ISU network (VPN if off campus).
See the [Sushi AI Server wiki page](https://github.com/anonymousgroundhog/ILSTU_Syllabus/wiki/Sushi-AI-Server)
for account setup and how to create an API key.

| File | What it does |
|------|--------------|
| `sushi_common.py` | Shared helpers: server URL, API key prompt, chat request |
| `send_text.py` | Send a text prompt, print the reply |
| `send_image.py` | Send a PNG image + question to a vision model, print the reply |
| `send_text_file.py` | Send a text file (inline or uploaded) + question, print the reply |
| `example_files/sample_image.png` | Sample image for `send_image.py` |
| `example_files/sample_log.txt` | Sample auth log for `send_text_file.py` |

## Setup

```bash
pip install -r requirements.txt
```

Your API key is **never** stored in the scripts. Either set it in your shell:

```bash
export SUSHI_API_KEY="sk-..."          # Linux/macOS
$env:SUSHI_API_KEY = "sk-..."          # Windows PowerShell
```

or leave it unset and each script will prompt you for it.

## Run

```bash
python send_text.py
python send_text.py "Explain file carving in two sentences." --model qwen3:latest

python send_image.py
python send_image.py my_screenshot.png "What error is shown?"

python send_text_file.py
python send_text_file.py my_notes.txt "Summarize this." --method upload
```

## Models

Default text model: `llama3.1:latest`. List all models with:

```bash
curl -H "Authorization: Bearer $SUSHI_API_KEY" http://sushi.it.ilstu.edu:8080/api/models
```

`llama3.1` is text-only, so `send_image.py` defaults to `llama3.2-vision:latest`.
Other vision models: `gemma3:latest`, `qwen3-vl:235b`.

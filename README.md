# YouTube Summary Generator

A tool that takes any YouTube video URL and generates a structured summary using AI — no manual watching required.

## Features

- Works with any YouTube video (long-form or Shorts)
- Automatically fetches the video transcript
- Falls back to non-English languages if English is unavailable
- Generates a structured summary: Overview, Key Points, and Conclusion
- Saves each summary as a `.txt` file named after the video

## Tech Stack

- **Python**
- **[youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api)** — fetches video transcripts
- **[Ollama](https://ollama.com)** (local AI) — generates the summary
- **Model:** `llama3.2`

## Project Structure

```
youtube-summary-generator/
+-- transcript.py       # Fetches video ID, title, and transcript from YouTube
+-- summarizer.py       # Sends transcript to Ollama and returns a structured summary
+-- main.py             # Entry point - orchestrates the full flow
+-- summaries/          # Output folder where generated summaries are saved
+-- requirements.txt
```

## Setup

**Prerequisites:**
- Python 3.10+
- [Ollama](https://ollama.com) installed and running
- `llama3.2` model pulled (`ollama pull llama3.2`)

**Install dependencies:**
```bash
uv venv
.venv\Scripts\activate    # Windows
source .venv/bin/activate # macOS/Linux
uv pip install -r requirements.txt
```

**Run:**
```bash
python main.py
```

You will be prompted to enter a YouTube URL. The summary will be printed to the terminal and saved to the `summaries/` folder.

## Roadmap

- [x] **Phase 1 - Local CLI:** Core logic with Ollama, summaries saved as `.txt` files
- [ ] **Phase 2 - Local Frontend:** Web UI to enter a URL and view the summary in the browser
- [ ] **Phase 3 - Production:** Hosted on Vercel with a cloud AI provider

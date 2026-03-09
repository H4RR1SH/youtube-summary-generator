# YouTube Summary Generator

A tool that takes any YouTube video URL and generates a structured summary using AI — no manual watching required.

**Live demo:** https://utubrief.onrender.com

## Features

- Works with any YouTube video (long-form or Shorts)
- Automatically fetches the video transcript
- Falls back to non-English languages if English is unavailable
- Generates a structured summary: Overview, Key Points, and Conclusion
- Clean web UI to enter a URL and view the summary in the browser

## Tech Stack

- **Python**
- **[FastAPI](https://fastapi.tiangolo.com)** — web framework
- **[Supadata](https://supadata.ai)** — fetches video transcripts (cloud-safe)
- **[Groq](https://groq.com)** — AI inference (model: `llama-3.3-70b-versatile`)
- **[Render](https://render.com)** — hosting

## Project Structure

```
youtube-summary-generator/
+-- backend/
|   +-- api.py          # FastAPI server and API routes
|   +-- transcript.py   # Fetches video ID, title, and transcript from YouTube
|   +-- summarizer.py   # Sends transcript to Groq and returns a structured summary
|   +-- main.py         # CLI entry point (Phase 1)
+-- frontend/
|   +-- index.html      # Web UI
|   +-- style.css       # Styling
|   +-- script.js       # Frontend logic
+-- summaries/          # Output folder for CLI-generated summaries
+-- render.yaml         # Render deployment config
+-- requirements.txt
```

## Local Setup

**Prerequisites:**
- Python 3.10+
- A [Groq API key](https://console.groq.com) (free)

**Install dependencies:**
```bash
uv venv
.venv\Scripts\activate    # Windows
source .venv/bin/activate # macOS/Linux
uv pip install -r requirements.txt
```

**Add your API keys** — create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_key_here
SUPADATA_API_KEY=your_supadata_key_here
```

**Run the web app:**
```bash
cd backend
uvicorn api:app --reload
```

Then open `http://localhost:8000` in your browser.

**Or run the CLI:**
```bash
cd backend
python main.py
```

## Roadmap

- [x] **Phase 1 - Local CLI:** Core logic with Ollama, summaries saved as `.txt` files
- [x] **Phase 2 - Local Frontend:** Web UI to enter a URL and view the summary in the browser
- [x] **Phase 3 - Production:** Hosted on Render with Groq AI

## Changelog

### 03-09-2026
- **Fixed video title display:** Switched from scraping the YouTube watch page (blocked by server environments) to the YouTube oEmbed API, so the real video title now shows correctly.
- **Improved summary accuracy:** Updated the AI prompt to handle auto-generated caption errors — the model now corrects garbled proper nouns and brand names using context.

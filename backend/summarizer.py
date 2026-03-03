import os
from groq import Groq
from dotenv import load_dotenv, find_dotenv

# Loads .env file if present (local dev), does nothing in production
load_dotenv(find_dotenv())


class SummarizerError(Exception):
    pass


_SYSTEM_PROMPT = """\
You are an expert at summarizing video content.
Given a YouTube video transcript, produce a structured summary in this exact format:

## Overview
A 2-3 sentence paragraph covering what the video is about.

## Key Points
- Key point 1
- Key point 2
- Key point 3
(add as many bullet points as needed)

## Conclusion
1-2 sentences on the main takeaway.

Be concise and accurate. Do not include information not present in the transcript.\
"""


def summarize(transcript_text: str, video_title: str) -> str:
    """Send the transcript to Groq and return the structured summary."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise SummarizerError("GROQ_API_KEY is not set.")

    client = Groq(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user",   "content": f'Video title: "{video_title}"\n\nTranscript:\n{transcript_text}'},
            ],
        )
    except Exception as e:
        raise SummarizerError(f"Groq request failed: {e}") from e

    return response.choices[0].message.content.strip()

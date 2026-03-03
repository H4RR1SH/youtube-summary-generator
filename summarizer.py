import ollama


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


def summarize(transcript_text: str, video_title: str, model: str = "llama3.2") -> str:
    """Send the transcript to Ollama and return the structured summary."""
    user_message = f'Video title: "{video_title}"\n\nTranscript:\n{transcript_text}'

    try:
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user",   "content": user_message},
            ],
        )
    except Exception as e:
        raise SummarizerError(f"Ollama request failed. Is Ollama running? Details: {e}") from e

    return response["message"]["content"].strip()

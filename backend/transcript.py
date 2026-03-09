import re
import os
import html
import requests
from supadata import Supadata
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


# --- Exceptions ---

class VideoIDError(Exception):
    pass

class NoTranscriptError(Exception):
    pass


# --- Video ID extraction ---

_ID_PATTERNS = [
    r'(?:v=)([A-Za-z0-9_-]{11})',
    r'(?:youtu\.be/)([A-Za-z0-9_-]{11})',
    r'(?:shorts/)([A-Za-z0-9_-]{11})',
    r'(?:embed/)([A-Za-z0-9_-]{11})',
    r'^([A-Za-z0-9_-]{11})$',
]

def extract_video_id(url: str) -> str:
    """Pull the 11-character video ID out of any YouTube URL format."""
    for pattern in _ID_PATTERNS:
        match = re.search(pattern, url.strip())
        if match:
            return match.group(1)
    raise VideoIDError(f"Could not find a video ID in: {url!r}")


# --- Title fetching ---

_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def fetch_video_title(video_id: str) -> str:
    """Fetch the video title via the YouTube oEmbed API."""
    try:
        response = requests.get(
            'https://www.youtube.com/oembed',
            params={'url': f'https://www.youtube.com/watch?v={video_id}', 'format': 'json'},
            headers=_HEADERS,
            timeout=10,
        )
        response.raise_for_status()
        title = response.json().get('title', '')
        if title:
            return re.sub(r'[\\/:*?"<>|]', '', html.unescape(title)).strip()[:200]
    except Exception:
        pass
    return video_id


# --- Transcript fetching ---

def get_transcript(video_id: str) -> tuple[str, str]:
    """Fetch transcript via Supadata and return (plain_text, language)."""
    api_key = os.environ.get("SUPADATA_API_KEY")
    if not api_key:
        raise NoTranscriptError("SUPADATA_API_KEY is not set.")

    client = Supadata(api_key=api_key)

    try:
        result = client.transcript(
            url=f"https://www.youtube.com/watch?v={video_id}",
            text=True,
        )
    except Exception as e:
        raise NoTranscriptError(f"Could not retrieve transcript: {e}")

    if not result.content:
        raise NoTranscriptError("No transcript available for this video.")

    return result.content, result.lang

import re
import html
import requests
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled


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
    """Scrape the video title from the YouTube watch page."""
    try:
        response = requests.get(f'https://www.youtube.com/watch?v={video_id}', headers=_HEADERS, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return video_id

    match = re.search(r'<title>(.+?) - YouTube</title>', response.text)
    if not match:
        match = re.search(r'"og:title" content="(.+?)"', response.text)

    if not match:
        return video_id

    title = html.unescape(match.group(1))
    # Remove characters that are not safe in filenames
    return re.sub(r'[\\/:*?"<>|]', '', title).strip()[:200]


# --- Transcript fetching ---

def get_transcript(video_id: str) -> tuple[str, str]:
    """
    Fetch transcript and return (plain_text, language_name).
    Tries English first, then lets the user pick from available languages.
    """
    try:
        transcript_list = YouTubeTranscriptApi().list(video_id)
    except TranscriptsDisabled:
        raise NoTranscriptError("Transcripts are disabled for this video.")
    except Exception as e:
        raise NoTranscriptError(f"Could not retrieve transcripts: {e}")

    # Try English first
    try:
        transcript = transcript_list.find_transcript(['en'])
        segments = transcript.fetch()
        return _segments_to_text(segments), transcript.language
    except NoTranscriptFound:
        pass

    # Fall back: list available languages and ask the user to pick
    available = list(transcript_list)
    if not available:
        raise NoTranscriptError("No transcripts available for this video.")

    print("\nNo English transcript found. Available languages:\n")
    for i, t in enumerate(available, start=1):
        tag = " [auto-generated]" if t.is_generated else ""
        print(f"  {i}. {t.language} ({t.language_code}){tag}")

    while True:
        raw = input("\nEnter the number of your chosen language: ").strip()
        try:
            choice = int(raw)
            if 1 <= choice <= len(available):
                chosen = available[choice - 1]
                segments = chosen.fetch()
                return _segments_to_text(segments), chosen.language
            print(f"Please enter a number between 1 and {len(available)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def _segments_to_text(segments) -> str:
    """Join transcript segments into a single plain-text string."""
    return " ".join(seg.text.replace("\n", " ").strip() for seg in segments if seg.text.strip())

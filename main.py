import os

from transcript import extract_video_id, fetch_video_title, get_transcript, VideoIDError, NoTranscriptError
from summarizer import summarize, SummarizerError

SUMMARIES_DIR = "summaries"


def save_summary(content: str, title: str) -> str:
    """Write the summary to a .txt file in the summaries folder, avoiding overwrites."""
    os.makedirs(SUMMARIES_DIR, exist_ok=True)
    path = os.path.join(SUMMARIES_DIR, f"{title}.txt")
    counter = 1
    while os.path.exists(path):
        path = os.path.join(SUMMARIES_DIR, f"{title} ({counter}).txt")
        counter += 1
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return os.path.abspath(path)


def main():
    print("YouTube Summary Generator")
    print("=" * 30)

    url = input("Enter a YouTube URL: ").strip()
    if not url:
        print("No URL entered.")
        return

    # Step 1: Extract video ID
    try:
        video_id = extract_video_id(url)
    except VideoIDError as e:
        print(f"\nError: {e}")
        return

    print(f"Video ID: {video_id}")

    # Step 2: Fetch title (falls back to video ID if unavailable)
    print("Fetching video title...", end=" ", flush=True)
    title = fetch_video_title(video_id)
    print(f"'{title}'")

    # Step 3: Get transcript
    print("Fetching transcript...", end=" ", flush=True)
    try:
        transcript_text, language = get_transcript(video_id)
        print(f"done ({language}).")
    except NoTranscriptError as e:
        print(f"\nError: {e}")
        return

    # Step 4: Summarize with Ollama
    print("Generating summary (this may take a moment)...", end=" ", flush=True)
    try:
        summary = summarize(transcript_text, title)
        print("done.")
    except SummarizerError as e:
        print(f"\nError: {e}")
        return

    # Step 5: Save to file
    saved_path = save_summary(summary, title)
    print(f"\nSummary saved to: {saved_path}")
    print("\n" + summary)


if __name__ == "__main__":
    main()

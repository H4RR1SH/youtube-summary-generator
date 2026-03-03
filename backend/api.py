from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from transcript import extract_video_id, fetch_video_title, get_transcript, VideoIDError, NoTranscriptError
from summarizer import summarize, SummarizerError

app = FastAPI()

FRONTEND_DIR = "../frontend"
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


class SummarizeRequest(BaseModel):
    url: str


@app.get("/")
def index():
    return FileResponse(f"{FRONTEND_DIR}/index.html")


@app.post("/summarize")
def summarize_video(request: SummarizeRequest):
    try:
        video_id = extract_video_id(request.url)
    except VideoIDError as e:
        raise HTTPException(status_code=400, detail=str(e))

    title = fetch_video_title(video_id)

    try:
        transcript_text, language = get_transcript(video_id)
    except NoTranscriptError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        summary = summarize(transcript_text, title)
    except SummarizerError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"title": title, "language": language, "summary": summary}

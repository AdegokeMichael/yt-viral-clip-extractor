from fastapi import FastAPI, Query
from pydantic import BaseModel
from download import download_video
from main import find_viral_moments, extract_clips, OUTPUT_DIR, DOWNLOAD_DIR
from pathlib import Path

app = FastAPI()

class ClipRequest(BaseModel):
    url: str
    top_n: int = 3
    duration: int = 10
    every_n_frames: int = 120

@app.post("/extract")
def extract_clips_api(req: ClipRequest):
    # Download video
    download_video(req.url)
    # Find the latest video file
    files = sorted(list(DOWNLOAD_DIR.glob("*.mp4")) + list(DOWNLOAD_DIR.glob("*.webm")), key=lambda f: f.stat().st_mtime, reverse=True)
    if not files:
        return {"error": "No downloaded video found."}
    video_path = files[0]
    # Find viral moments
    moments = find_viral_moments(video_path, top_n=req.top_n)
    # Extract clips
    extract_clips(video_path, moments, duration=req.duration)
    # Return paths to clips
    clips = [str(f) for f in OUTPUT_DIR.glob(f"{video_path.stem}clip*.mp4")]
    return {"clips": clips}
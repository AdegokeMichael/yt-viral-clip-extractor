import cv2
import torch
import numpy as np
from pathlib import Path
from tools import DOWNLOAD_DIR, OUTPUT_DIR, get_video_id
from transformers import CLIPProcessor, CLIPModel
import subprocess

# Load CLIP
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def extract_frames(video_path, every_n_frames=30):
    cap = cv2.VideoCapture(str(video_path))
    frames = []
    timestamps = []
    fps = cap.get(cv2.CAP_PROP_FPS)
    count = 0
    success, frame = cap.read()
    while success:
        if count % every_n_frames == 0:
            timestamp = count / fps
            frames.append(frame)
            timestamps.append(timestamp)
        success, frame = cap.read()
        count += 1
    cap.release()
    return frames, timestamps

def rank_frames(frames):
    prompts = ["exciting", "emotional", "shocking", "funny", "surprising"]
    inputs = processor(text=prompts, images=frames, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image
    scores = logits_per_image.softmax(dim=1).max(dim=1).values
    return scores.tolist()

def find_viral_moments(video_path, top_n=3):
    frames, timestamps = extract_frames(video_path)
    scores = rank_frames(frames)
    ranked = sorted(zip(timestamps, scores), key=lambda x: x[1], reverse=True)
    return [timestamp for timestamp, score in ranked[:top_n]]

def extract_clips(video_path: Path, moments: list, duration=10):
    for i, timestamp in enumerate(moments):
        output_file = OUTPUT_DIR / f"{video_path.stem}clip{i+1}.mp4"
        subprocess.run([
            "./extract_clip.sh",
            str(video_path),
            str(timestamp),
            str(duration),
            str(output_file)
        ], check=True)
        print(f"[🎞] Extracted clip: {output_file}")

if __name__ == "__main__":
    video_url = input("Enter YouTube video URL: ").strip()
    get_video_id(video_url)
    from download import download_video
    download_video(video_url)

    # Find the downloaded file
    downloaded_files = sorted(DOWNLOAD_DIR.glob("*.mp4"), key=lambda f: f.stat().st_mtime, reverse=True)
    video_path = downloaded_files[0] if downloaded_files else None

    if video_path:
        print(f"[🔍] Analyzing: {video_path}")
        moments = find_viral_moments(video_path)
        extract_clips(video_path, moments)
    else:
        print("[❌] No downloaded video found.")
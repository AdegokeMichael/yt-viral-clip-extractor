import cv2
import torch
import numpy as np
from pathlib import Path
from tools import DOWNLOAD_DIR, OUTPUT_DIR, get_video_id, create_directories
from transformers import CLIPProcessor, CLIPModel
import subprocess

# Load CLIP
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def extract_frames(video_path, every_n_frames=120):
    cap = cv2.VideoCapture(str(video_path))
    frames = []
    timestamps = []
    fps = cap.get(cv2.CAP_PROP_FPS)
    count = 0
    success, frame = cap.read()
    while success:
        if count % every_n_frames == 0:
            timestamp = count / fps
            # Resize frame to 224x224 for CLIP
            frame = cv2.resize(frame, (224, 224))
            frames.append(frame)
            timestamps.append(timestamp)
        success, frame = cap.read()
        count += 1
    cap.release()
    return frames, timestamps

def rank_frames(frames, batch_size=32):
    prompts = ["exciting", "emotional", "shocking", "funny", "surprising"]
    scores = []
    for i in range(0, len(frames), batch_size):
        batch = frames[i:i+batch_size]
        inputs = processor(text=prompts, images=batch, return_tensors="pt", padding=True)
        outputs = model(**inputs)
        logits_per_image = outputs.logits_per_image
        batch_scores = logits_per_image.softmax(dim=1).max(dim=1).values
        scores.extend(batch_scores.tolist())
    return scores

def find_viral_moments(video_path, top_n=3):
    frames, timestamps = extract_frames(video_path)
    scores = rank_frames(frames)
    ranked = sorted(zip(timestamps, scores), key=lambda x: x[1], reverse=True)
    return [timestamp for timestamp, score in ranked[:top_n]]

def extract_clips(video_path: Path, moments: list, duration=10):
    for i, timestamp in enumerate(moments):
        output_file = OUTPUT_DIR / f"{video_path.stem}clip{i+1}.mp4"
        subprocess.run([
            "ffmpeg",
            "-ss", str(timestamp),
            "-i", str(video_path),
            "-t", str(duration),
            "-c", "copy",
            str(output_file)
        ], check=True)
        print(f"[🎞] Extracted clip: {output_file}")

if __name__ == "__main__":
    create_directories()  # Ensure directories exist
    video_url = input("Enter YouTube video URL: ").strip()
    get_video_id(video_url)
    from download import download_video
    download_video(video_url)

    print("DEBUG: DOWNLOAD_DIR absolute path =", DOWNLOAD_DIR.resolve())  
    print("DEBUG: OUTPUT_DIR absolute path =", OUTPUT_DIR.resolve())
    print("DEBUG: All files in downloads:", [str(f) for f in DOWNLOAD_DIR.iterdir()])   

    # Find the downloaded file
    downloaded_files = sorted(
        list(DOWNLOAD_DIR.glob("*.mp4")) + list(DOWNLOAD_DIR.glob("*.webm")),
        key=lambda f: f.stat().st_mtime,
        reverse=True
    )
    print("DEBUG: Files found in downloads:", [str(f) for f in downloaded_files])
    video_path = downloaded_files[0] if downloaded_files else None
    print(f"DEBUG: video_path = {video_path}")

    if video_path:
        print(f"[🔍] Analyzing: {video_path}")
        moments = find_viral_moments(video_path)
        extract_clips(video_path, moments)
    else:
        print("[❌] No downloaded video found.")
        print("DEBUG: DOWNLOAD_DIR =", DOWNLOAD_DIR)
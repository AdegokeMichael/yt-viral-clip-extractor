import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

DOWNLOAD_DIR = Path(os.getenv("DOWNLOAD_DIR", "downloads"))
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "clips"))

def create_directories():
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def get_video_id(url: str) -> str:
    if "v=" in url:
        return url.split("v=")[-1].split("&")[0]
    return url.split("/")[-1]
import argparse
import subprocess
from tools import DOWNLOAD_DIR, create_directories, get_video_id

def download_video(url: str):
    create_directories()
    output_template = str(DOWNLOAD_DIR / "%(title)s.%(ext)s")
    cmd = [
        "yt-dlp",
        "-o", output_template,
        url
    ]
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download videos from YouTube")
    parser.add_argument("url", help="YouTube video URL")
    args = parser.parse_args()

    try:
        download_video(args.url)
        print(f"[✅] Download complete for {args.url}")
    except subprocess.CalledProcessError:
        print("[❌] Download failed.")
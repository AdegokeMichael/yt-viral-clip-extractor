# YouTube Viral Clip Extractor

Extracts viral moments from YouTube videos using OpenAI CLIP and saves them as short clips.

## Features

- Downloads YouTube videos using `yt-dlp`
- Analyzes video frames with CLIP to find exciting, emotional, shocking, funny, or surprising moments
- Extracts top moments as short video clips using `ffmpeg`
- Dockerized for easy setup and reproducibility

## Requirements

- Python 3.10+
- [ffmpeg](https://ffmpeg.org/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- See `requirements.txt` for Python dependencies

## Usage

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/yt-viral-clip-extractor.git
cd yt-viral-clip-extractor
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the script

```bash
python main.py
```
Enter the YouTube video URL when prompted.

### 4. Download videos directly

```bash
python download.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### 5. Docker usage

Build the Docker image:
```bash
docker build -t yt-viral-clip-extractor .
```

Run the container:
```bash
docker run -it --rm yt-viral-clip-extractor
```

## Output

- Downloaded videos are saved in the `downloads/` directory.
- Extracted clips are saved in the `clips/` directory.

## Configuration

- You can set custom download and output directories via environment variables:
  - `DOWNLOAD_DIR`
  - `OUTPUT_DIR`

## Notes

- For long videos, increase the frame sampling rate in `main.py` for faster analysis.
- Make sure your machine has enough RAM and CPU for CLIP processing.
- See `.gitignore` for recommended files/folders to exclude from version control.

## License

MIT

---

**Contributions welcome!**

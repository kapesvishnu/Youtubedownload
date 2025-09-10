# YouTube Downloader

A simple web-based YouTube video downloader with high-quality options and language support.

## Features

- Download YouTube videos in multiple quality options (1080p+, 720p, 480p, 360p)
- Telugu and English voice translation support
- No thumbnail downloads (removed as requested)
- Clean web interface
- Paste link and download functionality

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and go to `http://localhost:5000`

## Usage

1. Paste a YouTube URL in the input field
2. Select desired video quality
3. Choose language option (Original, Telugu, English)
4. Click "Download Video"
5. The video will be downloaded to your device

## Requirements

- Python 3.7+
- Flask
- yt-dlp
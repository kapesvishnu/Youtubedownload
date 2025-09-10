import yt_dlp
import os

def download_with_telugu_audio(url):
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
        'format': 'best[height<=1080]/best[height<=720]/best',
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['te', 'hi', 'en', 'auto'],
        'extractor_args': {'youtube': {'player_client': ['web', 'android', 'ios']}},
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get('title', 'video')
        
    print(f"Downloaded: {title}")
    
    # Check for Telugu subtitles
    for file in os.listdir('.'):
        if '.te.' in file and file.endswith('.srt'):
            print(f"Telugu subtitles found: {file}")
        elif '.hi.' in file and file.endswith('.srt'):
            print(f"Hindi subtitles found: {file}")

# Usage
url = "https://youtube.com/clip/Ugkxc_BgHuImmppZN5z3oIRGRkUNSS-C-AGW?si=yBmeEcDxeBwLM0jr"
download_with_telugu_audio(url)
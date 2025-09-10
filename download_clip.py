import yt_dlp
import os

url = "https://youtube.com/clip/Ugkxc_BgHuImmppZN5z3oIRGRkUNSS-C-AGW?si=yBmeEcDxeBwLM0jr"

ydl_opts = {
    'outtmpl': '%(title)s.%(ext)s',
    'format': 'best[height<=1080]/best[height<=720]/best',
    'extractor_args': {'youtube': {'player_client': ['web', 'android', 'ios']}},
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

print("Download completed!")
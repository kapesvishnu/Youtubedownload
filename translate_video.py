import yt_dlp
from googletrans import Translator
import subprocess
import os

def download_with_translation(url, target_lang='te'):
    translator = Translator()
    
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
        'format': 'best[height<=1080]/best[height<=720]/best',
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en', 'auto'],
        'extractor_args': {'youtube': {'player_client': ['web', 'android', 'ios']}},
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get('title', 'video')
    
    # Find subtitle file
    srt_file = None
    for file in os.listdir('.'):
        if file.endswith('.en.srt') or file.endswith('.auto.srt'):
            srt_file = file
            break
    
    if srt_file:
        # Translate subtitles
        with open(srt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        translated = translator.translate(content, dest=target_lang)
        
        with open(f'{title}_{target_lang}.srt', 'w', encoding='utf-8') as f:
            f.write(translated.text)
        
        print(f"Translation completed: {title}_{target_lang}.srt")
    else:
        print("No subtitles found for translation")

# Usage
url = "https://youtube.com/clip/Ugkxc_BgHuImmppZN5z3oIRGRkUNSS-C-AGW?si=yBmeEcDxeBwLM0jr"
download_with_translation(url, 'te')  # Telugu
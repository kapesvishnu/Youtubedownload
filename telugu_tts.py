import yt_dlp
import os
from gtts import gTTS
from googletrans import Translator
import re

def extract_text_from_vtt(vtt_file):
    with open(vtt_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove VTT formatting and extract text
    lines = content.split('\n')
    text_lines = []
    for line in lines:
        if '-->' not in line and not line.startswith('WEBVTT') and line.strip():
            clean_line = re.sub(r'<[^>]+>', '', line)  # Remove HTML tags
            if clean_line.strip():
                text_lines.append(clean_line.strip())
    
    return ' '.join(text_lines)

def download_and_translate_to_telugu(url):
    # Download video with subtitles
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
    vtt_file = None
    for file in os.listdir('.'):
        if title in file and file.endswith('.vtt'):
            vtt_file = file
            break
    
    if vtt_file:
        # Extract text from subtitles
        text = extract_text_from_vtt(vtt_file)
        
        # Translate to Telugu
        translator = Translator()
        translated = translator.translate(text, dest='te')
        
        # Convert to speech
        tts = gTTS(text=translated.text, lang='te')
        audio_file = f"{title}_telugu_audio.mp3"
        tts.save(audio_file)
        
        print(f"Telugu audio created: {audio_file}")
        return audio_file
    else:
        print("No subtitles found")
        return None

# Usage
url = "https://youtube.com/clip/Ugkxc_BgHuImmppZN5z3oIRGRkUNSS-C-AGW?si=yBmeEcDxeBwLM0jr"
download_and_translate_to_telugu(url)
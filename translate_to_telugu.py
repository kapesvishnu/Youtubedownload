import yt_dlp
import os
from gtts import gTTS
import requests
import re

def extract_text_from_vtt(vtt_file):
    with open(vtt_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    text_lines = []
    for line in lines:
        if '-->' not in line and not line.startswith('WEBVTT') and line.strip():
            clean_line = re.sub(r'<[^>]+>', '', line)
            if clean_line.strip():
                text_lines.append(clean_line.strip())
    
    return ' '.join(text_lines)

def translate_text(text, target_lang='te'):
    # Using MyMemory Translation API (free)
    url = f"https://api.mymemory.translated.net/get?q={text}&langpair=en|{target_lang}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['responseData']['translatedText']
    return text

def create_telugu_translation(url):
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
    
    vtt_file = None
    for file in os.listdir('.'):
        if title in file and file.endswith('.vtt'):
            vtt_file = file
            break
    
    if vtt_file:
        english_text = extract_text_from_vtt(vtt_file)
        print(f"Original text: {english_text[:100]}...")
        
        # Translate to Telugu
        telugu_text = translate_text(english_text)
        print(f"Telugu text: {telugu_text[:100]}...")
        
        # Create Telugu audio
        tts = gTTS(text=telugu_text, lang='te')
        audio_file = f"{title}_telugu_translation.mp3"
        tts.save(audio_file)
        
        print(f"Telugu translation audio created: {audio_file}")
        return audio_file
    else:
        print("No subtitles found")
        return None

url = "https://youtube.com/clip/Ugkxc_BgHuImmppZN5z3oIRGRkUNSS-C-AGW?si=yBmeEcDxeBwLM0jr"
create_telugu_translation(url)
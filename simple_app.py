from flask import Flask, request, jsonify, send_file
import yt_dlp
import os
import tempfile
from pathlib import Path
from gtts import gTTS
import requests
import re

app = Flask(__name__)

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
    # Limit text length for faster processing
    if len(text) > 500:
        text = text[:500] + "..."
    
    try:
        url = f"https://api.mymemory.translated.net/get?q={text}&langpair=en|{target_lang}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data['responseData']['translatedText']
    except:
        pass
    return text

@app.route('/')
def index():
    with open('index.html', 'r') as f:
        return f.read()

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get('url')
    translate_to_telugu = data.get('telugu', False)
    
    if not url:
        return "URL is required", 400
    
    try:
        temp_dir = tempfile.mkdtemp()
        
        ydl_opts = {
            'outtmpl': f'{temp_dir}/video.%(ext)s',
            'format': 'best[height<=1080]/best',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            'extractor_args': {'youtube': {'player_client': ['web', 'android', 'ios']}},
        }
        
        if translate_to_telugu:
            ydl_opts.update({
                'writesubtitles': True,
                'writeautomaticsub': True,
                'subtitleslangs': ['en', 'auto'],
            })
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'video')
        
        if translate_to_telugu:
            # Find subtitle file
            vtt_file = None
            for file in Path(temp_dir).glob('*.vtt'):
                vtt_file = str(file)
                break
            
            if vtt_file:
                english_text = extract_text_from_vtt(vtt_file)
                telugu_text = translate_text(english_text)
                
                # Save Telugu translation as text file
                text_file = f'{temp_dir}/telugu_translation.txt'
                with open(text_file, 'w', encoding='utf-8') as f:
                    f.write(f"Original: {english_text}\n\nTelugu Translation:\n{telugu_text}")
                
                return send_file(text_file, as_attachment=True, download_name=f'{title}_telugu.txt')
        
        # Find the downloaded video file
        files = list(Path(temp_dir).glob('*.mp4'))
        video_file = files[0] if files else None
        
        if not video_file:
            return "Download failed", 500
        
        return send_file(str(video_file), as_attachment=True, download_name='video.mp4')
        
    except Exception as e:
        return f"Error: {str(e)}", 500

# For Vercel
app = app

if __name__ == '__main__':
    app.run(debug=True, port=9090)
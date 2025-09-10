from flask import Flask, request, jsonify, send_file, render_template_string
import yt_dlp
import os
import tempfile
from pathlib import Path

app = Flask(__name__)

@app.route('/')
def index():
    with open('index.html', 'r') as f:
        return f.read()

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get('url')
    quality = data.get('quality', 'best')
    language = data.get('language', 'original')
    
    if not url:
        return "URL is required", 400
    
    try:
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        
        # Configure yt-dlp options (absolutely no ffmpeg)
        ydl_opts = {
            'outtmpl': f'{temp_dir}/%(title)s.%(ext)s',
            'writethumbnails': False,
            'writesubtitles': False,
            'writeautomaticsub': False,
            'format': '18',  # MP4 360p format that doesn't need ffmpeg
            'no_warnings': True,
            'prefer_ffmpeg': False,
        }
        
        # Handle language options (simplified implementation)
        if language == 'telugu':
            ydl_opts['writesubtitles'] = True
            ydl_opts['subtitleslangs'] = ['te', 'tel']
        elif language == 'english':
            ydl_opts['writesubtitles'] = True
            ydl_opts['subtitleslangs'] = ['en']
        
        # Download video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Find downloaded file
        files = list(Path(temp_dir).glob('*'))
        video_file = None
        for file in files:
            if file.suffix in ['.mp4', '.webm', '.mkv', '.avi']:
                video_file = file
                break
        
        if not video_file:
            return "Download failed", 500
        
        return send_file(str(video_file), as_attachment=True, download_name='video.mp4')
        
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, port=9000)
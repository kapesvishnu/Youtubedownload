from flask import Flask, request, jsonify

app = Flask(__name__)

def handler(request):
    if request.method == 'GET':
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>YouTube Downloader</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
                input, button { padding: 10px; margin: 10px 0; width: 100%; }
                button { background: #ff0000; color: white; border: none; cursor: pointer; }
            </style>
        </head>
        <body>
            <h1>YouTube Downloader</h1>
            <input type="url" id="url" placeholder="Paste YouTube URL">
            <button onclick="download()">Get Download Link</button>
            <div id="result"></div>
            
            <script>
            function download() {
                const url = document.getElementById('url').value;
                window.open('https://loader.to/api/button/?url=' + encodeURIComponent(url) + '&f=mp4&color=ff0000', '_blank');
            }
            </script>
        </body>
        </html>
        '''
    
    return 'Method not allowed', 405
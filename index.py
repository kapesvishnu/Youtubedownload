from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>YouTube Downloader</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
                input, button { padding: 15px; margin: 10px 0; width: 100%; font-size: 16px; }
                button { background: #ff0000; color: white; border: none; cursor: pointer; border-radius: 5px; }
                button:hover { background: #cc0000; }
            </style>
        </head>
        <body>
            <h1>YouTube Downloader</h1>
            <input type="url" id="url" placeholder="Paste YouTube URL here">
            <button onclick="download()">Download Video</button>
            
            <script>
            function download() {
                const url = document.getElementById('url').value;
                if (!url) {
                    alert('Please enter a YouTube URL');
                    return;
                }
                window.open('https://loader.to/api/button/?url=' + encodeURIComponent(url) + '&f=mp4&color=ff0000', '_blank');
            }
            </script>
        </body>
        </html>
        '''
        
        self.wfile.write(html.encode())
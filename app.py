from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json

app = Flask(__name__)
CORS(app)

@app.route('/api/download', methods=['POST'])
def download():
    try:
        data = request.get_json()
        url = data.get("url")

        # yt-dlp CLI command to get JSON info
        command = ['yt-dlp', '-j', url]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            return jsonify({'error': result.stderr.strip()})

        info = json.loads(result.stdout)

        formats = []
        for f in info.get('formats', []):
            if f.get('url') and f.get('ext') == 'mp4' and f.get('acodec') != 'none':
                formats.append({
                    'format': f"{f.get('format_note', 'unknown')} - {f.get('height')}p",
                    'url': f['url']
                })

        return jsonify({
            'title': info.get('title'),
            'thumbnail': info.get('thumbnail'),
            'links': formats[:5]
        })

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
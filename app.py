import os
from flask import Flask, jsonify
import serverless_wsgi

app = Flask(__name__)

# Cari lokasi absolut folder 'stories' di server Netlify
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
STORIES_DIR = os.path.join(BASE_DIR, 'stories')

# 1. API buat SCAN folder untuk side menu
@app.route('/api/list-stories')
def list_stories():
    try:
        # Scan semua subfolder di dalam folder 'stories'
        folders = [f for f in os.listdir(STORIES_DIR) if os.path.isdir(os.path.join(STORIES_DIR, f))]
        return jsonify({"status": "success", "folders": folders})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 2. API buat BACA isi file saat diklik
@app.route('/api/read-story/<folder_name>/<file_name>')
def read_story(folder_name, file_name):
    file_path = os.path.join(STORIES_DIR, folder_name, file_name)
    
    # Keamanan: pastikan file beneran ada dan jalurnya gak ngaco
    if os.path.exists(file_path) and file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({"status": "success", "content": content})
    else:
        return jsonify({"status": "error", "message": "Cerita nggak ketemu, Bro!"}), 404

def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)

import os
import re
from flask import Flask, jsonify, render_template, send_from_directory

app = Flask(__name__)

# Menentukan lokasi folder penyimpanan cerita novel
STORIES_DIR = os.path.join(app.root_path, 'stories')

# 1. API untuk men-scan folder dan list bab secara otomatis (Urut Alfabetis)
@app.route('/api/stories')
def get_stories():
    if not os.path.exists(STORIES_DIR):
        return jsonify([])

    story_list = []
    
    # Men-scan semua item di dalam folder 'stories' secara alfabetis (A-Z)
    for folder_name in sorted(os.listdir(STORIES_DIR)):
        folder_path = os.path.join(STORIES_DIR, folder_name)
        
        # Pastikan hanya folder yang diproses
        if os.path.isdir(folder_path):
            chapters = []
            
            # Men-scan file .txt di dalam folder novel tersebut
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.txt'):
                    # Mengambil angka bab menggunakan Regex
                    match = re.search(r'\d+', file_name)
                    if match:
                        chapters.append(int(match.group()))
            
            # Urutkan nomor bab dari terkecil ke terbesar
            chapters.sort()
            
            # Mengubah garis bawah menjadi spasi untuk judul di sidebar
            story_title = folder_name.replace('_', ' ')
            
            story_list.append({
                "story_title": story_title,
                "folder_name": folder_name,
                "chapters": chapters
            })
            
    return jsonify(story_list)

# 2. API untuk mengambil isi teks dari bab tertentu
@app.route('/api/text/<folder_name>/<int:chapter_number>')
def get_chapter_text(folder_name, chapter_number):
    filename = f"Chapter_{chapter_number}.txt"
    chapter_path = os.path.join(STORIES_DIR, folder_name)
    return send_from_directory(chapter_path, filename)

# 3. Rute utama untuk memuat halaman web pembaca novel
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
from flask import Flask, request, jsonify
import cloudinary
import cloudinary.uploader
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Configurar Cloudinary (substitua pelos seus dados)
cloudinary.config(
    cloud_name = 'dk89d49gv',
    api_key = '152896376356339',
    api_secret = 'ayaGH2aJmzhcYShhLl_DbQ49Sm8',
    secure = True
)

# Criar DB simples SQLite (se não existir)
def init_db():
    conn = sqlite3.connect('videos.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            url TEXT,
            upload_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/upload', methods=['POST'])
def upload():
    if 'video' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400

    video = request.files['video']

    # Upload para Cloudinary
    result = cloudinary.uploader.upload_large(video.stream, resource_type="video")

    url = result.get('secure_url')

    # Salvar no DB
    conn = sqlite3.connect('videos.db')
    c = conn.cursor()
    c.execute('INSERT INTO videos (filename, url, upload_date) VALUES (?, ?, ?)', 
              (video.filename, url, datetime.now().isoformat()))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Vídeo enviado com sucesso!', 'url': url})

@app.route('/videos')
def videos():
    conn = sqlite3.connect('videos.db')
    c = conn.cursor()
    c.execute('SELECT id, filename, url, upload_date FROM videos ORDER BY upload_date DESC')
    videos_list = c.fetchall()
    conn.close()

    return jsonify([{'id': v[0], 'filename': v[1], 'url': v[2], 'upload_date': v[3]} for v in videos_list])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

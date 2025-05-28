from flask import Flask, request, send_from_directory, render_template_string
import os
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    # Lista os arquivos na pasta de uploads
    files = os.listdir(UPLOAD_FOLDER)
    files = [f for f in files if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))]

    # Template HTML simples com links para as imagens
    html = """
    <h1>Imagens Salvas</h1>
    <ul>
        {% for file in files %}
        <li><a href="{{ url_for('serve_file', filename=file) }}" target="_blank">{{ file }}</a></li>
        {% endfor %}
    </ul>
    """
    return render_template_string(html, files=files)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return 'Nenhuma imagem enviada', 400
    image = request.files['image']
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    filename = f"{timestamp}_{image.filename}"
    path = os.path.join(UPLOAD_FOLDER, filename)
    image.save(path)
    return f'Imagem {filename} salva com sucesso!', 200

@app.route("/uploads/<path:filename>")
def serve_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

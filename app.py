#servidor flask

from flask import Flask, request
import os
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return 'Servidor online!'

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

if __name__ == '__main__':
    app.run(host='0.0.0.0')

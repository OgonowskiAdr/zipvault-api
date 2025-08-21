from flask import Flask, request, send_file
from flask_cors import CORS
import pyminizip
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/create-zip', methods=['POST'])
def create_zip():
    uploaded_file = request.files.get('file')
    password = request.form.get('password', '1234')

    if not uploaded_file:
        return {"error": "No file provided"}, 400

    original_filename = uploaded_file.filename
    input_path = f"/tmp/{original_filename}"
    zip_name = os.path.splitext(original_filename)[0] + ".zip"
    zip_path = f"/tmp/{zip_name}"

    # Zapisz plik tymczasowo
    uploaded_file.save(input_path)

    # Stwórz archiwum ZIP z hasłem
    pyminizip.compress(input_path, None, zip_path, password, 5)

    # Usuń plik źródłowy
    os.remove(input_path)

    # Wyślij ZIP jako odpowiedź
    return send_file(zip_path, as_attachment=True, download_name=zip_name)

@app.route('/api/health', methods=['GET'])
def health():
    return {"status": "healthy"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

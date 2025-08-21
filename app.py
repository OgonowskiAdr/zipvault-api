from flask import Flask, request, send_file
from flask_cors import CORS
import zipfile
import uuid
import os
import io

app = Flask(__name__)
CORS(app)

@app.route('/api/create-zip', methods=['POST'])
def create_zip():
    uploaded_file = request.files.get('file')
    password = request.form.get('password', '1234')

    if not uploaded_file:
        return {"error": "No file provided"}, 400

    temp_id = str(uuid.uuid4())
    input_path = f"/tmp/{temp_id}_{uploaded_file.filename}"
    zip_path = f"/tmp/{temp_id}.zip"

    # Zapisz plik tymczasowo
    uploaded_file.save(input_path)

    # Spakuj plik z hasłem i oryginalną nazwą
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.setpassword(password.encode())
        zipf.write(input_path, arcname=uploaded_file.filename)

    os.remove(input_path)
    return send_file(zip_path, as_attachment=True)

@app.route('/api/health', methods=['GET'])
def health():
    return {"status": "healthy"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

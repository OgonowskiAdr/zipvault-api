from flask import Flask, request, send_file
import pyminizip
import uuid
import os

app = Flask(__name__)

@app.route('/api/create-zip', methods=['POST'])
def create_zip():
    uploaded_file = request.files.get('file')
    password = request.form.get('password', '1234')
    if not uploaded_file:
        return {"error": "No file provided"}, 400

    temp_id = str(uuid.uuid4())
    input_path = f"/tmp/{temp_id}_{uploaded_file.filename}"
    zip_path = f"/tmp/{temp_id}.zip"

    uploaded_file.save(input_path)
    pyminizip.compress(input_path, None, zip_path, password, 5)
    os.remove(input_path)

    return send_file(zip_path, as_attachment=True)

@app.route('/api/health', methods=['GET'])
def health():
    return {"status": "healthy"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

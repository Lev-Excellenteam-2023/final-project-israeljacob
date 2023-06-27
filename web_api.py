import glob
import os
import uuid
from datetime import datetime
import json

from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'


def get_file_details(filename):
    filename = os.path.basename(filename)
    parts = filename.split('_')
    original_filename = '_'.join(parts[:-2])
    timestamp = datetime.strptime(parts[-2], '%Y%m%d%H%M%S')
    uid = parts[-1].split('.')[0]
    return original_filename, timestamp, uid


@app.route('/', methods=['POST'])
def upload():
    """
    Handle file upload.

    This route receives a file through a POST request and saves it to the server.

    Returns:
        A JSON response containing the unique identifier (uid) of the uploaded file,
        or an error message if no file was uploaded.
    """

    file = request.files['file']
    if file:
        uid = str(uuid.uuid4())
        original_filename = file.filename
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        new_filename = f'{original_filename}_{timestamp}_{uid}'
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
        return jsonify({'uid': uid})
    return jsonify({'error': 'No file uploaded.'})


@app.route('/<uid>', methods=['GET'])
def status(uid):
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    matching_files = [file for file in files if uid in file]
    if len(matching_files) == 0:
        return jsonify({
            'status': 'not found',
            'filename': None,
            'timestamp': None,
            'explanation': None
        }), 404

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], matching_files[0])
    original_filename, timestamp, _ = get_file_details(matching_files[0])

    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            explanation = json.load(f)
        status = 'done'
    else:
        explanation = None
        status = 'pending'

    return jsonify({
        'status': status,
        'filename': original_filename,
        'timestamp': timestamp,
        'explanation': explanation
    }), 200


if __name__ == '__main__':
    app.run()

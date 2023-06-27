import glob
import os
import uuid
from datetime import datetime
import json

from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'


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


if __name__ == '__main__':
    app.run()

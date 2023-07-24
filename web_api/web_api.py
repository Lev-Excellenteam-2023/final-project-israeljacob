import os
import uuid
from datetime import datetime
import json
from sqlalchemy import select

from typing import Union
from flask import Flask, request, jsonify
from sqlalchemy.orm import Session
import db.orm

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'C:\\users\\yisra\\desktop\\uploads'


def get_file_details(filename: str) -> tuple:
    """
    Extracts details from a filename.

    Args:
        filename (str): The filename to extract details from.

    Returns:
        tuple: A tuple containing the original filename, timestamp, and UID.
    """
    filename = os.path.basename(filename)
    parts = filename.split('_')
    original_filename = '_'.join(parts[:-2])
    timestamp = datetime.strptime(parts[-2], '%Y%m%d%H%M%S')
    uid = parts[-1].split('.')[0]
    return original_filename, timestamp, uid


@app.route('/upload', methods=['POST'])
def upload() -> jsonify:
    """
    Handle file upload.

    This route receives a file through a POST request and saves it to the server.

    Returns:
        A JSON response containing the unique identifier (uid) of the uploaded file,
        or an error message if no file was uploaded.
    """

    file = request.files['file']
    email = request.form.get('email')

    if file:
        uid = str(uuid.uuid4())
        engine = db.orm.engine
        with Session(engine) as session:
            new_upload = db.orm.Upload(uid=uid, original_filename=file.filename.split('.pptx')[0],
                      timestamp=datetime.now().strftime('%Y%m%d%H%M%S'), status='Pending')
            session.add(new_upload)
            session.commit()

        new_filename = f'{uid}.pptx'
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))

        if email:
            user = get_user_by_email(email, session)
            if not user:
                user = db.orm.User(email = email)
            user.uploads.append(new_upload)
            new_upload.user = user
            new_upload.user_id = user.id
            session.add_all([user, new_upload])
            session.commit()
        return jsonify({'uid': uid})
    return jsonify({'error': 'No file uploaded.'})


@app.route('/status/<uid_filename_email>', methods=['GET'])
def status(uid_filename_email: str) -> jsonify:
    """
    Retrieve file status and explanation.

    This route retrieves the status and explanation of a file with the given UID.

    Args:
        uid (str): The unique identifier (UID) of the file.

    Returns:
        jsonify: A JSON response containing the status, original filename, timestamp,
        and explanation (if available) of the file.
    """
    if uid_filename_email.__contains__('@'):
        
    files = os.listdir('C:\\users\\yisra\\desktop\\uploads')
    matching_files = [file for file in files if uid_filename_email + ".pptx" == file.split("_")[2]]
    if len(matching_files) == 0:
        return jsonify({
            'status': 'not found',
            'filename': None,
            'timestamp': None,
            'explanation': None
        }), 404

    file_path = os.path.join('C:\\users\\yisra\\desktop\\outputs', matching_files[0])
    file_path = file_path.split(".pptx")[0] + ".json"

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


def get_user_by_email(email, session: Session) -> Union[db.orm.User, None]:
    select_statement = select(db.orm.User).where(db.orm.User.email == email)
    result = session.scalars(select_statement).all()
    if result:
        return result[0]
    else:
        return None


if __name__ == '__main__':
    app.run(host='127.0.0.1')

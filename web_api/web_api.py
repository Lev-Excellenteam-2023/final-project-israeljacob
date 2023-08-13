import os
import uuid
from datetime import datetime
import json
from sqlalchemy import select
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
                user = db.orm.User(email=email)
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
        uid_filename_email (str): The unique identifier (UID) of the file.

    Returns:
        jsonify: A JSON response containing the status, original filename, timestamp,
        and explanation (if available) of the file.
    """
    session = Session(db.orm.engine)
    if not uid_filename_email.__contains__('@'):
        requested_upload = get_upload_by_uid(uid_filename_email, session)
        if not requested_upload:
            return jsonify({
                'status': 'not found',
                'filename': None,
                'timestamp': None,
                'explanation': None
            }), 404

    else:
        filename, email = uid_filename_email.split(' ')
        user = get_user_by_email(email, session)
        if not user:
            return jsonify({
                'status': 'not found',
                'filename': None,
                'timestamp': None,
                'explanation': None
            }), 404
        requested_upload = get_latest_upload_by_user(user)

    if requested_upload.status == 'done':
        file_path = os.path.join('C:\\users\\yisra\\desktop\\outputs', requested_upload.filename)
        file_path = file_path.split(".pptx")[0] + ".json"
        with open(file_path, 'r') as f:
            explanation = json.load(f)
    else:
        explanation = None

    return jsonify({
        'status': requested_upload.status,
        'filename': requested_upload.original_filename,
        'timestamp': requested_upload.timestamp,
        'explanation': explanation
    }), 200


def get_user_by_email(check_email, session: Session) -> db.orm.User:
    select_statement = select(db.orm.User).where('email' == check_email)
    result = session.scalars(select_statement).all()
    if result:
        return result[0]
    else:
        return None


def get_upload_by_uid(uid, session: Session) -> db.orm.Upload:
    select_statement = select(db.orm.Upload).where('uid' == uid)
    result = session.scalars(select_statement).all()
    if result:
        return result[0]
    else:
        return None


def get_latest_upload_by_user(user) -> db.orm.Upload:
    return max([uploads for uploads in user.uploads])


if __name__ == '__main__':
    app.run(host='127.0.0.1')

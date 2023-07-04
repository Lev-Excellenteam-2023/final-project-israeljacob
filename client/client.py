import requests
from datetime import datetime


def upload_file(base_url, file_path):
    """
    Uploads a file to the web app.

    Args:
        base_url (str): The base URL of the web app.
        file_path (str): The path of the file to upload.

    Returns:
        str: The UID (unique identifier) of the uploaded file.

    Raises:
        requests.HTTPError: If the upload request fails or returns an error.

    """

    url = f"{base_url}/upload"
    response = requests.post(url, files={'file': open(file_path, 'rb')})
    response.raise_for_status()
    json_data = response.json()
    return json_data['uid']


def get_status(base_url, uid):
    """
    Retrieves the status of a file from the web app.

    Args:
        base_url (str): The base URL of the web app.
        uid (str): The UID (unique identifier) of the file.

    Returns:
        dict: A dictionary containing the status information.

    Raises:
        requests.HTTPError: If the status request fails or returns an error.

    """

    url = f"{base_url}/status/{uid}"
    response = requests.get(url)
    response.raise_for_status()
    json_data = response.json()
    status = json_data['status']
    filename = json_data['filename']
    timestamp = json_data['timestamp']
    explanation = json_data['explanation']
    return {
        'status': status,
        'filename': filename,
        'timestamp': timestamp,
        'explanation': explanation
    }


def is_done(status):
    """
    Checks if the file processing is done based on the status information.

    Args:
        status (dict): A dictionary containing the status information.

    Returns:
        bool: True if the status is 'done', False otherwise.

    """
    return status['status'] == 'done'

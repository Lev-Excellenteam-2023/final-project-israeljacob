import time
from client import client

# Base URL of the Web API
base_url = 'http://127.0.0.1:5000'

# Path of the sample presentation to upload
sample_presentation_path = 'C:/Users/yisra/Desktop/to_pass/study/lev/year 3/tt.pptx'


def run_system_test():
    # Upload the sample presentation
    print("Uploading the sample presentation...")
    uid = client.upload_file(base_url, sample_presentation_path)
    print("Sample presentation uploaded. UID:", uid)

    # Wait for the file processing to complete
    while True:
        status = client.get_status(base_url, uid)
        if client.is_done(status):
            break
        print("File processing is still in progress. Waiting...")
        time.sleep(5)

    # File processing is done
    print("File processing is complete.")
    print("Status:", status['status'])
    print("Original Filename:", status['filename'])
    print("Timestamp:", status['timestamp'])
    print("Explanation:", status['explanation'])


if __name__ == '__main__':
    run_system_test()

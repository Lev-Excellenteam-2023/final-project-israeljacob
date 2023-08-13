import datetime
import os
import time

from sqlalchemy import select
from sqlalchemy.orm import Session

from extract_text_from_pptx import extract_text_from_pptx
from openAI_calls import call_openai_api_helper
from export_to_json import write_to_json
from db.orm import *
import asyncio

UPLOADS_FOLDER = 'C:\\users\\yisra\\desktop\\uploads'
OUTPUTS_FOLDER = 'C:\\users\\yisra\\desktop\\outputs'


def get_files_for_taking_care():
    select_statement = select(Upload).where(Upload.status == 'pending')
    result = Session(engine).scalars(select_statement).all()
    if result:
        return result
    else:
        return None


def treat_file(upload):
    """
    Processes a PowerPoint file by extracting text, making OpenAI API calls, and writing the results to a JSON file.

    Args:
        upload (str): Path of the PowerPoint file to be processed.

    Returns:
        None

    """
    uploaded_file = [upload_file for upload_file in os.listdir(UPLOADS_FOLDER) if upload_file.endswith(upload.filename + ".pptx")][0]
    pptx_text_dict = extract_text_from_pptx(uploaded_file)
    openai_returned_dict = asyncio.run(call_openai_api_helper(pptx_text_dict))
    upload.finish_time = datetime.datetime.now()
    upload.status = 'done'
    file_name = os.path.basename(upload)
    file_path = os.path.join(OUTPUTS_FOLDER, file_name)
    write_to_json(file_path, pptx_text_dict, openai_returned_dict)


def run_explainer():
    """
    Runs the explainer application by continuously monitoring the uploads folder and processing new PowerPoint files.

    Returns:
        None

    """

    os.makedirs(OUTPUTS_FOLDER, exist_ok=True)
    try:
        while True:
            files_for_taking_care = get_files_for_taking_care()
            for upload in files_for_taking_care:
                print(f"Starting to treat upload {upload.filename} \n")
                treat_file(upload)
                print(f"Finished treating upload {upload.filename} \n")
            time.sleep(10)
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    run_explainer()

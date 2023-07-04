import os
import time
from extract_text_from_pptx import extract_text_from_pptx
from openAI_calls import call_openai_api_helper
from export_to_json import write_to_json
import asyncio

UPLOADS_FOLDER = 'C:\\users\\yisra\\desktop\\uploads'
OUTPUTS_FOLDER = 'C:\\users\\yisra\\desktop\\outputs'


def treat_file(file):
    """
    Processes a PowerPoint file by extracting text, making OpenAI API calls, and writing the results to a JSON file.

    Args:
        file (str): Path of the PowerPoint file to be processed.

    Returns:
        None

    """

    pptx_text_dict = extract_text_from_pptx(file)
    openai_returned_dict = asyncio.run(call_openai_api_helper(pptx_text_dict))
    file_name = os.path.basename(file)
    file_path = os.path.join(OUTPUTS_FOLDER, file_name)
    write_to_json(file_path,pptx_text_dict, openai_returned_dict)


def run_explainer():
    """
    Runs the explainer application by continuously monitoring the uploads folder and processing new PowerPoint files.

    Returns:
        None

    """

    files_was_treated = []
    os.makedirs(OUTPUTS_FOLDER, exist_ok=True)
    try:
        while True:
            files_for_taking_care = [file for file in os.listdir(UPLOADS_FOLDER)
                                     if file.endswith(".pptx") and file not in files_was_treated]
            for file in files_for_taking_care:
                print(f"Starting to treat file {file} \n")
                file = os.path.join(UPLOADS_FOLDER,file)
                treat_file(file)
                print(f"Finished treating file {file} \n")
            files_was_treated += files_for_taking_care
            time.sleep(10)
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    run_explainer()

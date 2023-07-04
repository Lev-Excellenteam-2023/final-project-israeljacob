import json


def save_dict_to_json(file_path: str, data: list):
    """
    Save a dictionary as JSON to a file.

    Parameters:
        file_path (str): The path of the JSON file to be created.
        data (list): The dictionary to be saved as JSON.

    Returns:
        None
    """
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=2)


def convert_dict_to_json_array(file_path: str, pptx_text_dict: dict, openai_returned_dict: dict):
    """
    Convert two dictionaries into a list of JSON objects and save it as a JSON array.

    Parameters:
        file_path (str): The path of the JSON file to be created.
        pptx_text_dict (dict): Dictionary containing slide numbers and original text from pptx.
        openai_returned_dict (dict): Dictionary containing slide numbers and OpenAI explanations.

    Returns:
        None
    """
    json_array = [
        {
            "slide number": key,
            "original text": pptx_text_dict[key],
            "explanation": value
        }
        for key, value in openai_returned_dict.items()
    ]
    save_dict_to_json(file_path, json_array)


def write_to_json(file_path: str, pptx_text_dict: dict, openai_returned_dict: dict):
    """
    Write two dictionaries as a JSON array to a file.

    Parameters:
        file_path (str): The path of the JSON file to be created.
        pptx_text_dict (dict): Dictionary containing slide numbers and original text from pptx.
        openai_returned_dict (dict): Dictionary containing slide numbers and OpenAI explanations.

    Returns:
        None
    """
    file_path = file_path.split('.')[0] + '.json'
    convert_dict_to_json_array(file_path, pptx_text_dict, openai_returned_dict)

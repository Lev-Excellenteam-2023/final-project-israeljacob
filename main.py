from extract_text_from_pptx import extract_text_from_pptx
from openAI_calls import call_openai_api_helper
from export_to_json import write_to_json
import asyncio


def main():
    pptx_path = input("Hi dear student. \n You missed a lecture in college? Don't worry.\n"
                      "Enter the path to the pptx file of the lecture and you will get a json file with explanation.")
    pptx_text_dict = extract_text_from_pptx(pptx_path)
    openai_returned_dict = asyncio.run(call_openai_api_helper(pptx_text_dict))
    write_to_json(pptx_path,pptx_text_dict, openai_returned_dict)


if __name__ == "__main__":
    main()

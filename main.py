import time

from extract_text_from_pptx import extract_text_from_pptx
from openAI_calls import call_openai_api_helper
import asyncio

loop = asyncio.get_event_loop()


def main():
    text_dict = extract_text_from_pptx("Longest Common Subsequence.pptx")
    returned_dict = asyncio.run(call_openai_api_helper(text_dict))
    print(returned_dict)


if __name__ == "__main__":
    main()

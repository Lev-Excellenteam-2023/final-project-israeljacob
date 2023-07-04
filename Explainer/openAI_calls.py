import openai
import asyncio

openai.api_key_path = '../API_KEY.txt'

prompt = "I have missed the lecture in college and I have just the text from the pptx file of the lecture. can you " \
         "explain me the text? here is the text:   "


async def call_openai_api(value: str) -> str:
    """
       Calls the OpenAI API to generate explanations for a given value.

       Parameters:
           value (str): The text value to be explained.

       Returns:
           str: The generated explanation.
       """
    response = await openai.Completion.acreate(engine='text-davinci-003', prompt= prompt + value, max_tokens=1000)
    return "".join(choice.text.strip() for choice in response.choices)


async def call_openai_api_helper(text_dict: dict) -> dict:
    """
        Calls the OpenAI API for multiple values and returns the explanations in a dictionary.

        Parameters:
            text_dict (dict): A dictionary with text values to be explained.

        Returns:
            dict: A dictionary containing the explanations for each input text.
        """
    returned_dict = {}
    for key, value in text_dict.items():
        returned_dict[key] = await call_openai_api(value)
    return returned_dict

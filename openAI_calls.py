import openai

openai.api_key_path = 'API_KEY.txt'

prompt = "I have missed the lecture in college and I have just the text from the pptx file of the lecture. can you " \
         "explain me the text? here is the text:"


def call_openai_api(text_dict: dict) ->dict:
    returned_dict = {}
    for key, value in text_dict.items():
        response = openai.Completion.create(engine='text-davinci-003',
                                            prompt=prompt + value,
                                            max_tokens=3000)
        returned_dict[key] = response.choices[0].text.strip()
    return returned_dict

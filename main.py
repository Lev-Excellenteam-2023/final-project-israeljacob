from extract_text_from_pptx import extract_text_from_pptx
from openAI_calls import call_openai_api


def main():
    text_dict = extract_text_from_pptx("Longest Common Subsequence.pptx")
    returned_dict = call_openai_api(text_dict)
    print(returned_dict)


if __name__ == "__main__":
    main()

# text_dict = extract_text_from_pptx("Longest Common Subsequence.pptx")
#
# async def generate_text(iterator_prompt):
#     response = await openai.Completion.create(
#         engine='text-davinci-003',
#         prompt=prompt + iterator_prompt,
#         max_tokens=3000
#     )
#     generated_text = response.choices[0].text.strip()
#     print(generated_text)
#
# async def main():
#     loop = asyncio.get_event_loop()
#     tasks = []
#     for iterator_prompt in text_dict.values():
#         task = loop.run_in_executor(None, generate_text, iterator_prompt)
#         tasks.append(task)
#     generated_texts = await asyncio.gather(*tasks)
#     for text in generated_texts:
#         print(text)
#
# if __name__ == "__main__":
#     asyncio.run(main())

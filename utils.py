# import openai
# import os
# from dotenv import load_dotenv
#
#
# load_dotenv()
# openai.api_key = os.getenv(OPENAI_KEY)
# openai.organization = os.getenv(OPENAI_ORG)
#
#
# def generate_description(input):
#     messages = [{"role": "user",
#                  "content": """As a Product Description Generator, Generate multi paragraph rich text product description with emojis from the information provided to you' \n"""},
#                 {"role": "user", "content": f"{input}"}]
#
#     completion = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=messages
#     )
#     reply = completion.choices[0].message.content
#     return reply

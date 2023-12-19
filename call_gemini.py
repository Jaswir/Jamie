import google.generativeai as genai
import os
from os import environ
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI


GOOGLE_API_KEY = environ.get("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# print(GOOGLE_API_KEY)

# message = HumanMessage(
#   content=[
#     {
#     "type": "text",
#     "text": "Which button should I press to mute the TV?",
#     }, # You can optionally provide text parts
#     {
#     "type": "image_url",
#     "image_url": "https://raw.githubusercontent.com/Jaswir/Jamie/main/Remote.jpeg"
#     },
#   ]
# )

# llm = ChatGoogleGenerativeAI (model="gemini-pro-vision", temperature=0.7)
# response = llm.invoke([message])
# print(response)




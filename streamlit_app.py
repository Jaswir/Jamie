import streamlit as st
from deepgram import Deepgram

import pyaudio
import wave
from gtts import gTTS

import google.generativeai as genai
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from trulens_eval.feedback.provider.openai import OpenAI as fOpenAI

import os
from os import environ
import json
import streamlit as st
from streamlit_javascript import st_javascript
from streamlit.components.v1 import html
import time
import datetime
import asyncio
import base64
import airtable

from st_audiorec import st_audiorec
from google.cloud import storage
from io import BytesIO

language = "en"

# Local
# GSC_CREDS_TYPE = environ.get("GSC_CREDS_TYPE")
# GSC_CREDS_TYPE_PROJECT_ID = environ.get("GSC_CREDS_TYPE_PROJECT_ID")
# GSC_CREDS_PRIVATE_KEY_ID = environ.get("GSC_CREDS_PRIVATE_KEY_ID")
# GSC_CREDS_PRIVATE_KEY = environ.get("GSC_CREDS_PRIVATE_KEY").replace("\\n", "\n")
# GSC_CREDS_CLIENT_EMAIL = environ.get("GSC_CREDS_CLIENT_EMAIL")
# GSC_CREDS_CLIENT_ID = environ.get("GSC_CREDS_CLIENT_ID")
# GSC_CREDS_CLIENT_X509_CERT_URL = environ.get("GSC_CREDS_CLIENT_X509_CERT_URL")

# environ["OPENAI_API_KEY"] = environ.get("OPEN_AI_KEY")
# DEEPGRAM_API_KEY = environ.get("DEEPGRAM_API_KEY")
# GOOGLE_API_KEY = environ.get("GOOGLE_API_KEY")

 # For live streamlit get env variable from secrets
GSC_CREDS_TYPE = st.secrets.GSC_CREDS_TYPE
GSC_CREDS_TYPE_PROJECT_ID = st.secrets.GSC_CREDS_TYPE_PROJECT_ID
GSC_CREDS_PRIVATE_KEY_ID = st.secrets.GSC_CREDS_PRIVATE_KEY_ID
GSC_CREDS_PRIVATE_KEY = st.secrets.GSC_CREDS_PRIVATE_KEY.replace("\\n", "\n")
GSC_CREDS_CLIENT_EMAIL = st.secrets.GSC_CREDS_CLIENT_EMAIL
GSC_CREDS_CLIENT_ID = st.secrets.GSC_CREDS_CLIENT_ID
GSC_CREDS_CLIENT_X509_CERT_URL = st.secrets.GSC_CREDS_CLIENT_X509_CERT_URL

environ["OPENAI_API_KEY"] = st.secrets["OPEN_AI_KEY"]
DEEPGRAM_API_KEY = st.secrets["DEEPGRAM_API_KEY"]
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

gsc_credentials_dict = {
  "type": GSC_CREDS_TYPE,
  "project_id": GSC_CREDS_TYPE_PROJECT_ID,
  "private_key_id": GSC_CREDS_PRIVATE_KEY_ID,
  "private_key": GSC_CREDS_PRIVATE_KEY,
  "client_email": GSC_CREDS_CLIENT_EMAIL,
  "client_id": GSC_CREDS_CLIENT_ID,
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": GSC_CREDS_CLIENT_X509_CERT_URL,
  "universe_domain": "googleapis.com"
}

json_data = json.dumps(gsc_credentials_dict, indent=4)
json_bytes = json_data.encode('utf-8')

with open("gsc_creds.json", mode="wb") as f:
    f.write(json_bytes)

environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'gsc_creds.json'

PATH_TO_FILE = "input.wav"
MIMETYPE = "audio/wav"

if "recorded" not in st.session_state:
    st.session_state.recorded = False

if "image_url" not in st.session_state:
    st.session_state.image_url = ""


def audioToText():
    dg_client = Deepgram(DEEPGRAM_API_KEY)
    with open(PATH_TO_FILE, "rb") as audio:
        source = {"buffer": audio, "mimetype": MIMETYPE}
        options = {"punctuate": False, "model": "enhanced", "language": language}

        print("Requesting transcript... \n")

        response = dg_client.transcription.sync_prerecorded(source, options)
        data = json.loads(json.dumps(response, indent=4))
        text = data["results"]["channels"][0]["alternatives"][0]["transcript"]

        return text


def getGeminiProResponse(text):
    genai.configure(api_key=GOOGLE_API_KEY)

    if st.session_state.image_url == "":
        mesg = "No image uploaded, please provide a jpg image"
        st.markdown(f"<br><h5>{mesg}</h5>", unsafe_allow_html=True)

    st_javascript(st.session_state.image_url)
    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": text,
            },  # You can optionally provide text parts
            {
                "type": "image_url",
                "image_url": st.session_state.image_url,
            },
        ]
    )

    llm = ChatGoogleGenerativeAI(model="gemini-pro-vision", temperature=0.7)
    print("Generating response...")
    response = llm.invoke([message])

    # print("\n Response::")
    # print(response)

    text = str(response)
    text = text.split("=")[1]

    return text


def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )


def convert_google_text_to_speech(text):
    tts = gTTS(text, lang=language)
    tts.save("output.mp3")


st.subheader("Jamie: AI voice assistant")
cul1, cul2, cul3 = st.columns([2, 1, 1])
cul1.image("banner_image.png")

uploaded_file = st.file_uploader("Choose an image file to upload", type="jpg")
if uploaded_file is not None:
    # Upload data to cloud storage service
    client = storage.Client()
    bucket = client.get_bucket("bucket-j20")

    # Save the file to directory
    with open(os.path.join("tmpDirUploadedImage", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())

    blob = bucket.blob(uploaded_file.name)
    blob.upload_from_filename("./tmpDirUploadedImage/" + uploaded_file.name)

    st.session_state.image_url = (
        "https://storage.googleapis.com/bucket-j20/" + uploaded_file.name
    )


wav_audio_data = st_audiorec()
if wav_audio_data is not None:
    with open("input.wav", mode="wb") as f:
        f.write(wav_audio_data)

    text = audioToText()
    print("Input text::", text)
    st.markdown(f"<br><h5>{text}</h5>", unsafe_allow_html=True)

    response = getGeminiProResponse(text)
    print("Got response from gemini", response)

    print("Converting text to speech...")
    convert_google_text_to_speech(response)

    # Evaluate response and log result in database.
    fopenai = fOpenAI()
    relevance = fopenai.relevance_with_cot_reasons(text, response)

    ACCESS_TOKEN = environ.get("AIRTABLE_ACCESS_TOKEN")
    # For live streamlit get env variable from secrets
    # ACCESS_TOKEN = st.secrets["AIRTABLE_ACCESS_TOKEN"]
    BASE_ID = "app3pk0rq2zPednxk"
    TABLE_NAME = "Table%201"

    at = airtable.Airtable(BASE_ID, ACCESS_TOKEN)
    at.create(
        TABLE_NAME,
        {
            "Relevance": str(relevance),
            "Prompt": text,
            "Response": response,
        },
    )

    st.session_state.input = text
    st.session_state.recorded = True


container_2 = st.empty()

if st.session_state.recorded:
    st.markdown("<h5>Response: </h5>", unsafe_allow_html=True)
    autoplay_audio("output.mp3")

    button_restart = container_2.button("Record again?")
    if button_restart:
        st.markdown('<meta http-equiv="refresh" content="0">', unsafe_allow_html=True)
        st.session_state.recorded = False
        st.session.ended = True

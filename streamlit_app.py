import streamlit as st
import pyaudio
import wave
from deepgram import Deepgram
from gtts import gTTS

import google.generativeai as genai
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from os import environ
import json
import streamlit as st
import time
import datetime
import asyncio
import base64


language = "en"

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
frames = []
seconds = 6
p = pyaudio.PyAudio()

DEEPGRAM_API_KEY = environ.get("DEEPGRAM_API_KEY")
PATH_TO_FILE = "input.wav"
MIMETYPE = "audio/wav"

if "recorded" not in st.session_state:
    st.session_state.recorded = False

def record_audio():
    print("start recording...")
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    for i in range(0, int(RATE / CHUNK * seconds)):
        data = stream.read(CHUNK)
        frames.append(data)
        secs = int(i / (RATE / CHUNK))
        mm, ss = secs // 60, secs % 60
        container.metric("Recording...", f"{mm:02d}:{ss:02d}")

    print("recording stopped")
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open("input.wav", "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()



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

    # Pass text to LLM
    GOOGLE_API_KEY = environ.get("GOOGLE_API_KEY")
    genai.configure(api_key=GOOGLE_API_KEY)

    message = HumanMessage(
    content=[
        {
        "type": "text",
        "text": text,
        }, # You can optionally provide text parts
        {
        "type": "image_url",
        "image_url": "https://raw.githubusercontent.com/Jaswir/Jamie/main/Remote.jpeg"
        },
    ]
    )

    llm = ChatGoogleGenerativeAI (model="gemini-pro-vision", temperature=0.7)
    print("Generating response...")
    response = llm.invoke([message])

    # print("\n Response::")
    # print(response)

    text = str(response)
    text = text.split('=')[1]

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



st.subheader("Jamie: A voice assistant")

container = st.empty()
container_2 = st.empty()


async def recording_time():
    button_start = container_2.button("Record")
    clock = f"{0:02d}:{0:02d}"
    if button_start:
        while True:
            
            button_start = container_2.button("Recording...")
            # record_audio()
            # text = audioToText()
            # print("Input text::", text)

            text = "How to mute the tv"

            # container.metric("Processing...", f"{0:02d}:{5:02d}")
            # button_start = container_2.button("Processing...", disabled=True)
            # text = "how to turn off the tv"
            # st.markdown(f"<br><h5>{text}</h5>", unsafe_allow_html=True)

            # response = getGeminiProResponse(text)
            # print("Got response from gemini", response)

            # print("Converting text to speech...")
            # convert_google_text_to_speech(response)

            st.session_state.recorded = True
            break

    else:
        container.metric("Ask me...", clock)
        


if not st.session_state.recorded:
    asyncio.run(recording_time())


if st.session_state.recorded:
    st.markdown("<h5>Response: </h5>", unsafe_allow_html=True)
    autoplay_audio("output.mp3")

    button_restart = container_2.button("Record again?")
    if button_restart:
        st.markdown('<meta http-equiv="refresh" content="0">', unsafe_allow_html=True)


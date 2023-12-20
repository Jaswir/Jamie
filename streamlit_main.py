import streamlit as st
import pyaudio
import wave
from deepgram import Deepgram
from playsound import playsound
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
import inspect
from audio_recorder_streamlit import audio_recorder

# Records Audio
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
frames = []
seconds = 6
p = pyaudio.PyAudio()

st.subheader("Jamie: A voice assistant")

container = st.empty()
container_2 = st.empty()

async def recording_time():
    button_start = container_2.button('Record')
    clock = f"{0:02d}:{0:02d}"
    if button_start:
        while True:
          
            #call recording function()
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
            break


    else:
        container.metric("Ask me...", clock)

asyncio.run(recording_time())


# container = st.empty()
# container_2 = st.empty()

# async def recording_time():
#     button_start = container_2.button('Record')
#     clock = f"{0:02d}:{0:02d}"
#     if button_start:
#         while True:
#             button_end = container_2.button('End')

#             #call recording function()

#             print("start recording...")

#             for secs in range(0, 10000, 1):
#                 mm, ss = secs // 60, secs % 60
#                 container.metric("Recording...", f"{mm:02d}:{ss:02d}")
#                 r = await asyncio.sleep(1)
#             if button_end:
#                 print("recording stopped")
#                 container_2.empty()
#                 button_start = container_2.button('Start')
#                 break

#     else:
#         container.metric("Ask me...", clock)

# asyncio.run(recording_time())

import pyaudio
import wave
from deepgram import Deepgram

import google.generativeai as genai
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from os import environ
import json


# Records Audio
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
p = pyaudio.PyAudio()

stream = p.open(
    format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
)

print("start recording...")
frames = []
seconds = 8
for i in range(0, int(RATE / CHUNK * seconds)):
    data = stream.read(CHUNK)
    frames.append(data)


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


#Converts Audio to Text
# The API key we created in step 3
DEEPGRAM_API_KEY = environ.get("DEEPGRAM_API_KEY")
PATH_TO_FILE = 'input.wav'
MIMETYPE = 'audio/wav'

def audioToText():

    dg_client = Deepgram(DEEPGRAM_API_KEY)
    with open(PATH_TO_FILE, 'rb') as audio:
        source = {'buffer': audio, 'mimetype': MIMETYPE}
        options = { "punctuate": False, "model": "enhanced", "language": "en" }

        print('Requesting transcript... \n')
      
    
        response = dg_client.transcription.sync_prerecorded(source, options)
        data = json.loads(json.dumps(response, indent=4))
        text = data["results"]["channels"][0]["alternatives"][0]["transcript"]

        return text


text = audioToText()
print("Input text", text)

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
print("\n")
print(response)




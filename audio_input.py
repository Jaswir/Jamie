import pyaudio
import wave
from deepgram import Deepgram
import json

# Records Audio
# CHUNK = 1024
# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 44100
# p = pyaudio.PyAudio()

# stream = p.open(
#     format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
# )

# print("start recording...")
# frames = []
# seconds = 8
# for i in range(0, int(RATE / CHUNK * seconds)):
#     data = stream.read(CHUNK)
#     frames.append(data)


# print("recording stopped")
# stream.stop_stream()
# stream.close()
# p.terminate()

# wf = wave.open("output.wav", "wb")
# wf.setnchannels(CHANNELS)
# wf.setsampwidth(p.get_sample_size(FORMAT))
# wf.setframerate(RATE)
# wf.writeframes(b"".join(frames))
# wf.close()


#Converts Audio to Text

# The API key we created in step 3
DEEPGRAM_API_KEY = '22adac15bb37b45f6da61911c61704ce30b01fa6'

PATH_TO_FILE = 'output.wav'
MIMETYPE = 'audio/wav'

def main():

    dg_client = Deepgram(DEEPGRAM_API_KEY)
    with open(PATH_TO_FILE, 'rb') as audio:
        source = {'buffer': audio, 'mimetype': MIMETYPE}
        options = { "punctuate": False, "model": "enhanced", "language": "nl" }

        print('Requesting transcript... \n')
      
    
        response = dg_client.transcription.sync_prerecorded(source, options)
        data = json.loads(json.dumps(response, indent=4))
        print(data["results"]["channels"][0]["alternatives"][0]["transcript"])


main()
from playsound import playsound 
from gtts import gTTS

text = "content=' De mute-knop bevindt zich linksonder op de afstandsbediening.'"
text = text.split('=')[1]

# Use Google Text to speech to convert text to speech
tts = gTTS(text, lang='nl')
tts.save("output.mp3")

# Provide the path to your sound file 
sound_file = "output.mp3" 
 
# Play the sound file 
playsound(sound_file) 
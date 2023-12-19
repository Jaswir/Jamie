import streamlit as st
from tempfile import NamedTemporaryFile
import os
import set_api_key
from call_gemini import call_gemini_vision

st.title("Visual Image Scenario Interpretation & Object Narration  (VISION)")


# clears temp folder of images
folder_path = "./temp"
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)


uploaded_file = st.file_uploader("Upload Image", type=['png', 'jpg'], accept_multiple_files=False, label_visibility="visible")
 
if uploaded_file is not None:
    with NamedTemporaryFile(prefix='C:/Users/futeb/Coding/github/GeminiVision/temp/', suffix=".jpg", delete=False,) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        temp_file_path = tmp_file.name
        st.write(temp_file_path)
    


if uploaded_file is not None:
    st.image(uploaded_file)


if uploaded_file is not None:
    user_input = st.text_input("Prompt", "Give me more context for this image")
    button = st.button("Gemini Vision")
    if button:
        response = call_gemini_vision(user_input)
        if response is not None:
            st.write(response)


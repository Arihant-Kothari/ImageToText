import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(
    page_title="Image-To-Story",
    page_icon=":frame_with_picture:"
)

hide_streamlit_style = """<style> #MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.markdown("""<style>.stApp a:first-child {display: none;}.css-15zrgzn {display: none}.css-eczf16 {display: none}.css-jn99sy {display: none}</style>""", unsafe_allow_html=True)
hide_decoration_bar_style ="""<style>header {visibility: hidden;}</style>"""
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)
st.write('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

st.title("Image-To-Story"+":frame_with_picture:"+":black_nib:")
st.button("Made By Arihant Kothari",disabled=True)

image = st.file_uploader("Upload An Image")

if image is not None:
    st.caption("Uploaded Image")
    st.image(image)

    tone=st.selectbox('Please Select Tone For The Story',
    ('--Select--','Dramatic','Emotional','Sad','Horror','Comedy'))
    audio = st.checkbox('Do You Want Audio?')

    if st.button('Submit'):
        with st.spinner('Generating Image Description..'):
            time.sleep(2)
        API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
        headers = {"Authorization": "Bearer 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"}
        response = requests.post(API_URL, headers=headers, data=image)
        output=response.json()
        st.caption("Image Description")
        st.info(output[0]['generated_text'])

        def genStory(text):
            API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
            headers = {"Authorization": "Bearer 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"}

            def query(payload):
                response = requests.post(API_URL, headers=headers, json=payload)
                return response.json()
            
            input=f"<|system|>You are an award winning writer</s><|user|>write a {tone} story,text: {text}</s><|writer|>"
        
            output = query({
                "inputs": input,
            })
            return [output,len(input)]

        def genAudio(text):
            CHUNK_SIZE = 1024
            url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"

            header = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": "a50e5a069e35caaf25785e9f5085e174"
            }

            data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
            }

            response = requests.post(url, json=data, headers=header)
            with open('output.mp3', 'wb') as f:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)

        if tone is not "--Select--":
            with st.spinner('Generating Story..'):
                time.sleep(2)
            output=genStory(output[0]['generated_text'])
            story=output[0][0]['generated_text'][output[1]+2:]
            st.caption("Generated Story")
            st.info(story)

        if audio:
            with st.spinner('Generating Audio..'):
                time.sleep(7)
            genAudio(output[0][0]['generated_text'][output[1]+2:])
            st.caption("Listen To Audio")
            st.audio("output.mp3")
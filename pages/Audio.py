
import os
import streamlit as st
from dotenv import load_dotenv
import config

import google.generativeai as genai

load_dotenv()

uploaded_file = st.file_uploader("Upload a file", type=["m4a","mp3"], accept_multiple_files=False)
# st.text(uploaded_files)

if 'transcription' not in st.session_state:
    st.session_state.transcription = None

if 'model' not in st.session_state:
    st.session_state.model = None

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message['role']):
        st.markdown(message['text'])

def upload_if_needed(pathname: str) -> str:
#    st.write('inside upload')
   api_key = os.getenv("GEMINI_API_LEY")
   genai.configure(api_key=api_key)
   
#    st.write("From upload_if_needed: ", pathname)
   uploaded_file = genai.upload_file(path=pathname, display_name="pathname")
#    st.write(uploaded_file)
#    st.write(uploaded_file.uri)

   model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=config.generation_config,
                              safety_settings=config.safety_settings)
   
   prompt = "Here is a audio recording of a conversation. Generate Transcript of the audio file accurately"
   
   response = model.generate_content([prompt, uploaded_file])
#    st.write(response.text)

   return model, response.text

def get_gemini_response(model, response, query):
    # st.write('from get_gemini_response, file; ', file)

    query_prefix = "Please answer the following question using the context from previous conversation only. \
    Focus on providing factual and relevant information based on the conversation in the transcript. \
    If the transcript doesn't contain enough information to answer the question, politely state that and suggest alternative ways to find the answer."

    modified_query = query_prefix + query

    convo = model.start_chat(history=[
        {
            "role": "model",
            "parts": response
        },

])
    convo.send_message(modified_query)
    # st.write(convo.last.text)
    return convo.last.text

if uploaded_file and st.session_state.transcription is None:
    with open(uploaded_file.name, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    model, response = upload_if_needed(uploaded_file.name)
    st.session_state.transcription = response
    st.session_state.model = model


# st.write(response)
if st.session_state.transcription:
    query=st.chat_input("Enter your quesion here... ",key="input")
    if query:
        with st.chat_message("user"):
            st.write(query) 

        st.session_state.chat_history.append({"role":'user', "text":query})


        gemini_response=get_gemini_response(st.session_state.model, st.session_state.transcription, query)
        with st.chat_message("assistant"):
            st.write(gemini_response) 

        st.session_state.chat_history.append({"role":'assistant', "text":gemini_response})
    
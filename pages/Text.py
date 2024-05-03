
import os
import streamlit as st
from dotenv import load_dotenv
import config
import google.generativeai as genai
import subprocess
from pdf2image import convert_from_path
import subprocess
import pathlib
import tqdm

load_dotenv()

selected_file = st.file_uploader("Upload a file", type=["pdf"], accept_multiple_files=False)
# st.text(extracted_data)

if 'extracted_data' not in st.session_state:
    st.session_state.extracted_data = None

if 'model' not in st.session_state:
    st.session_state.model = None

if 'text_chat_history' not in st.session_state:
    st.session_state.text_chat_history = []

for message in st.session_state.text_chat_history:
    with st.chat_message(message['role']):
        st.markdown(message['text'])


def extract_data_from_pdf(pdf_path, first_page, last_page, output_dir):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    poppler_path = r'C:\Users\saika\New\Portfolio\Hackathons\Hackathon_Google\Release-24.02.0-0\poppler-24.02.0\Library\bin'

    images = convert_from_path(pdf_path, first_page=first_page, last_page=last_page, poppler_path=poppler_path)
    # Save images to output directory
    for i, image in enumerate(images):
        image_path = f"{output_dir}/images-{i + 1}.jpeg"
        image.save(image_path, "JPEG")

    pdftotext_executable = os.path.join(poppler_path, "pdftotext.exe")
    # Extract text for each page in the specified range
    for page_number in range(first_page, last_page + 1):
        page_number_str = f"{page_number:03d}"
        subprocess.run([pdftotext_executable, pdf_path, '-f', str(page_number), '-l', str(page_number), f'{output_dir}/text-{page_number_str}.txt'])

    
    api_key = os.getenv("GEMINI_API_LEY")
    genai.configure(api_key=api_key)

    files = []
    image_files = list(pathlib.Path("output").glob('images-*.jpeg'))
    for img in tqdm.tqdm(image_files):
        files.append(genai.upload_file(img))

    # print('files: ', files)    

    texts = [t.read_text(encoding='utf-8') for t in pathlib.Path("output").glob('text-*.txt')]
    # print('texts: ', texts)


    textbook = []
    for page, (text, image) in enumerate(zip(texts, files)):
        print()
        textbook.append(f'## Page {page} ##')
        textbook.append(text)
        textbook.append(image)

    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=config.generation_config,
                              safety_settings=config.safety_settings)

    return textbook, model

def get_gemini_response(model, extracted_data, query):
    # st.write('from get_gemini_response, file; ', file)

    query_prefix = "# Please answer the following question using the given context. Focus on providing factual and relevant information based on the context. \
    If the context doesn't contain enough information to answer the question, politely state that and suggest alternative ways to find the answer. Context: "

    response = model.generate_content([query_prefix] + extracted_data + ["END\n\n"] + [query])
#    st.write(response.text)

    return response.text

if selected_file and st.session_state.extracted_data is None:
    with open(selected_file.name, 'wb') as f:
        f.write(selected_file.getbuffer())

    st.write('Please provide the starting and ending page number from which you want to ask questions')
    first_page = st.number_input("Insert a number", key="first_page", value=None, step = 1)
    last_page = st.number_input("Insert a number", key="last_page", value=None, step = 1)
    if first_page is not None and last_page is not None: 
        extracted_data, model = extract_data_from_pdf(selected_file.name, first_page, last_page, "output")
        st.session_state.extracted_data = extracted_data
        st.session_state.model = model


# st.write(response)
if st.session_state.extracted_data:
    query=st.chat_input("Enter your quesion here... ",key="input")
    if query:
        with st.chat_message("user"):
            st.write(query) 

        st.session_state.text_chat_history.append({"role":'user', "text":query})

        gemini_response=get_gemini_response(st.session_state.model, st.session_state.extracted_data, query)
        with st.chat_message("assistant"):
            st.write(gemini_response) 

        st.session_state.text_chat_history.append({"role":'assistant', "text":gemini_response})
    
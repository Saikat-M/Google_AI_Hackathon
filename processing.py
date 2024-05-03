from pdf2image import convert_from_path
import os
import subprocess
import pathlib
import tqdm
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def extract_data_from_pdf(pdf_path, first_page, last_page, output_dir):
#     # Create output directory if it doesn't exist
#     os.makedirs(output_dir, exist_ok=True)

#     poppler_path = r'C:\Users\saika\New\Portfolio\Hackathons\Hackathon_Google\Release-24.02.0-0\poppler-24.02.0\Library\bin'

#     images = convert_from_path(pdf_path, first_page=first_page, last_page=last_page, poppler_path=poppler_path)
#     # Save images to output directory
#     for i, image in enumerate(images):
#         image_path = f"{output_dir}/images-{i + 1}.jpeg"
#         image.save(image_path, "JPEG")

#     pdftotext_executable = os.path.join(poppler_path, "pdftotext.exe")
#     # Extract text for each page in the specified range
#     for page_number in range(first_page, last_page + 1):
#         page_number_str = f"{page_number:03d}"
#         subprocess.run([pdftotext_executable, pdf_path, '-f', str(page_number), '-l', str(page_number), f'{output_dir}/text-{page_number_str}.txt'])

    
#     api_key = os.getenv("GEMINI_API_LEY")
#     genai.configure(api_key=api_key)

#     files = []
#     image_files = list(pathlib.Path("output").glob('images-*.jpeg'))
#     for img in tqdm.tqdm(image_files):
#         files.append(genai.upload_file(img))

#     print('files: ', files)    

#     texts = [t.read_text(encoding='utf-8') for t in pathlib.Path("output").glob('text-*.txt')]
#     print('texts: ', texts)


#     textbook = []
#     for page, (text, image) in enumerate(zip(texts, files)):
#         print()
#         textbook.append(f'## Page {page} ##')
#         textbook.append(text)
#         textbook.append(image)

#     print('textbook: ', textbook)
    print(len(pdf_path))

# Example usage
pdf_path = "AI and Machine Learning for Coders.pdf"
first_page = 100  # Change to the desired first page number
last_page = 110  # Change to the desired last page number
output_dir = "output"  # Output directory for text files

extract_data_from_pdf(pdf_path, first_page, last_page, output_dir)


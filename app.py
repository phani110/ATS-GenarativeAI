import base64
import io
from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def get_gemini_response(input,pdf_content,prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    reponse = model.generate_content([input,pdf_content[0],prompt]);
    return reponse.text;

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
    
        first_page = images[0]
    
        #convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr,format = 'JPEG')
        img_byte_arr = img_byte_arr.getvalue()
    
        pdf_parts = [
            {
                "mime_type" : "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
    
        return pdf_parts
    else:
        raise FileNotFoundError("No File uploaded")
    
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area('Job Description: ',key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")
    
submit1 = st.button("Tell Me About the Resume")

submit2 = st.button("Percentage Match")        

input_prompt1 = """
You are an experienced Technical Human Resource Manager in the field of Data Science, Full Stack Web Development, Devops, Cloud Engineer, your task is to review the provided resume against the job description. Please share your professional evaluation on whether the candidate's profile aligns with Highlight the strengths and weaknesses of the applicant in relation to the specific job.
"""

input_prompt2 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of Data Science, Web Development, Devops Cloud Engineer, your task is to evaluate the resume against the provided job description. give me the job description. First the output should come as percentage and then keywords missing and final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        reponse=get_gemini_response(input_text,pdf_content,input_prompt1)
        st.subheader("The response is")
        st.write(reponse)
    else:
        st.write("Please upload the resume")
elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        reponse=get_gemini_response(input_text,pdf_content,input_prompt2)
        st.subheader("The response is")
        st.write(reponse)
    else:
        st.write("Please upload the resume")              
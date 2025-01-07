import fitz  # PyMuPDF
import base64
import streamlit as st
import os
import io
from PIL import Image 
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
api_key="AIzaSyC8sJ_4sP20KiY-Ai7TmeXXDEhz7PCDgXo"
model_config = {
  "temperature": 0.2,
  "top_p": 0.99,
  "top_k": 0,
  "max_output_tokens": 4096,
}
model = genai.GenerativeModel('gemini-1.5-flash', generation_config=model_config)

def get_gemini_response(input_text, pdf_text, prompt, ):
    response = model.generate_content([input_text, pdf_text, prompt])
    return response.text


def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Open the PDF file
        pdf_text = ""
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            # Extract text from each page
            for page_num in range(len(doc)):
                page = doc[page_num]
                pdf_text += page.get_text()

        # Prepare text in required format
        pdf_parts = [{"mime_type": "text/plain", "data": base64.b64encode(pdf_text.encode()).decode()}]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit App

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage match")
submit4=st.button("Tailor your resume")

input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description.If the total experience required for the job does not match
then give the percentage as 0 percent and specify the reason.Else Give me the percentage of match if the resume matches
the job description. First, the output should come as a percentage, then missing keywords, and finally, final thoughts..
"""

input_prompt4="""
You are an expert career consultant with in-depth knowledge of Applicant Tracking Systems (ATS) and resume optimization. Given the following job description and user resume, your task is to revise the resume so that it aligns more closely with the job description, improves relevance, and passes ATS screening effectively. Follow these instructions:
Identify Key Skills and Keywords: Analyze the job description to identify essential skills, keywords, and qualifications, and ensure these are incorporated naturally and contextually into the resume.
Revise Experience and Achievements: Rewrite job titles, responsibilities, and achievements in the resume to emphasize experience and skills that match the job description’s requirements. Highlight any relevant accomplishments that demonstrate the user’s qualifications.
Use ATS-friendly Formatting: Ensure the language and structure are straightforward and compatible with ATS, avoiding special characters, tables, and non-standard fonts that may hinder parsing.
Focus on Quantifiable Results: Where applicable, add measurable outcomes to previous job roles (e.g., "increased sales by 20%" or "reduced processing time by 30%") to demonstrate impact effectively.
Add Missing Relevant Sections or Keywords: If there are relevant sections (such as “Technical Skills” or “Certifications”) missing in the resume, add these sections as appropriate. Include any additional keywords or skills necessary to align with the job description
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content[0]["data"], input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content[0]["data"], input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload the resume")
elif submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt4, pdf_content[0]["data"], input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload the resume")

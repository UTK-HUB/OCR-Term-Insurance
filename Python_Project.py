import streamlit as st
from PIL import Image
import pytesseract
import pdfminer
import pdf2image
from pdfminer.high_level import extract_text
from pdf2image import convert_from_bytes
import re
import os
import tempfile


st.sidebar.image("https://zfunds-public.s3.ap-south-1.amazonaws.com/articlesImage/1621222010425")
st.sidebar.image("https://www.maxlifeinsurance.com/static-page/assets/homepage/must_know_life_insurance_policy_mobile_6f5e0911bc_290fa26dd8.webp")

st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Max_Life_Insurance_logo.svg/2560px-Max_Life_Insurance_logo.svg.png",width=150)
st.title("Welcome To Maxlife Term Insurance")
st.subheader("Overview :")
("""Term life insurance is a type of policy that provides coverage for a specific period, or "term," typically ranging from 10 to 30 years. 
It is a pure-protection life insurance policy where you pay a premium in exchange for coverage. If the insured individual passes away during 
the term, the policy pays out a death benefit to the beneficiaries. Term insurance is straightforward, offering coverage without accumulating 
cash value.""")
st.subheader("How It Works?")
("- Premiums : Policyholders pay premiums for the chosen term.")
("- Coverage : If the insured dies during the term, beneficiaries receive a death benefit.")
("- No Cash Value : Unlike whole life insurance, term insurance does not accumulate cash value.")
st.subheader("What Are the Types?")
("- Level Term : Offers a fixed premium and death benefit throughout the policy term.")
("- Decreasing Term : Death benefit decreases over time, often used for mortgage protection.")
("- Renewable Term : Allows policy renewal at the end of the term without a medical exam.")
("- Convertible Term : Permits conversion to permanent life insurance during the term.")

path=r"C:\Users\utkar\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd=path

name = st.text_input("Enter your name : ").split()

def main():
    doc = ["Select Document","Aadhar Card Image","PAN Card Image","Salary Slip PDF"]
    choice = st.sidebar.selectbox("Upload required documents :",doc)
    if choice == "PAN Card Image":
        load_pan_image()
    elif choice == "Aadhar Card Image":
        load_aadhar_image()
    elif choice == "Salary Slip PDF":
        load_salary_pdf()
            

def load_aadhar_image():
    st.subheader("Aadhar Card")
    uploaded_image = st.sidebar.file_uploader("Upload Aadhar Card Image", type=["jpg", "jpeg", "png"])
    if uploaded_image is not None:
        st.image(uploaded_image, caption="Uploaded Aadhar Card Image", width=250)
        temp_dir = tempfile.mkdtemp()
        path = os.path.join(temp_dir, uploaded_image.name)
        with open(path, "wb") as f:
            f.write(uploaded_image.getvalue())
        text = pytesseract.image_to_string(path)
        Name = re.search(r"[A-Z]+[a-z]+.\s[A-Z]+[a-z]+.\s[A-Z]+[a-z]+.\s[A-Z]+[a-z]+.\b",text)
        dob = re.search(r"\b\d{1,2}[/]\d{1,2}[/]\d{4}\b",text)
        aadhar = re.search(r"\b\d{4}\s\d{4}\s\d{4}\b",text)
        Extrated_name = Name.group().split("\n")
        st.write(f"Name : {Extrated_name[1]}")
        st.write(f"Date of Birth : {dob.group()}")
        st.write(f"Aadhar Number : {aadhar.group()}")
    
def load_pan_image():
    st.subheader("PAN Card")
    uploaded_image = st.sidebar.file_uploader("Upload PAN Card Image", type=["jpg", "jpeg", "png"])
    if uploaded_image is not None:
        st.image(uploaded_image, caption="Uploaded PAN Card Image", width=250)
        text1 = pytesseract.image_to_string(Image.open(uploaded_image))
        Pan_no = re.search(r"\b[A-Z]{5}\d{4}[A-z]\b",text1)
        dob = re.search(r"\b\d{1,2}[/]\d{1,2}[/]\d{4}\b",text1)
        st.write(f"PAN Card Number : {Pan_no.group()}")
        st.write(f"Date of Birth : {dob.group()}")

path_pop = r"C:\Program Files\poppler-23.11.0\Library\bin"

def load_salary_pdf():
    st.subheader("Salary Slip")
    uploaded_pdf = st.sidebar.file_uploader("Upload Salary Slip PDF", type="pdf")
    if uploaded_pdf is not None:
        if uploaded_pdf.type == "application/pdf":
            pdf_image = convert_from_bytes(uploaded_pdf.read(),poppler_path = path_pop)
            for i in pdf_image:
                st.image(i, width=500)
        text2 = extract_text(uploaded_pdf)
        Salary = re.findall(r"\b\d{5,6}\b(?=)",text2)
        st.write(f"Monthly Salary : {Salary.pop()}")

main()
st.image("https://static.pbcdn.in/cdn/images/bu/term/type-of-max-life-insurance-plans-desktop.png",width=800)

# importing required modules
from pypdf import PdfReader
import google.generativeai as genai

def send_query(prompt_path,cv_path):
    query = format_query(prompt_path,cv_path)
    print(query)
    genai.configure(api_key="AIzaSyCdosn5Pm4cVw5xKVa-XoGtSdBeGhotZJY")
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(query)
    return response

def extract_text_from_pdf(path):
    # creating a pdf reader object
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        # getting a specific page from the pdf file
        text += page.extract_text()
    return(text)

def format_query(prompt_path,cv_path):
    with open(prompt_path, "r") as file:
        prompt = file.read()
    cv = extract_text_from_pdf(cv_path)
    query = (
        "<instructions>\n"
        f"{prompt}"
        "\n</instructions>"
        "\n<cv>"
        f"f{cv}"
        "\n</cv>"
    )
    return  query

from cv_analyzer import extract_text_from_pdf, format_query
from tests import *
from cv_analyzer import *
import google.generativeai as genai


genai.configure(api_key="AIzaSyCdosn5Pm4cVw5xKVa-XoGtSdBeGhotZJY")

model = genai.GenerativeModel('gemini-2.0-flash')

#paths:
prompt_path =  "prompts/readability score prompt.txt"
cv_path = 'cvs/cv-01.pdf'
response = send_query(prompt_path,cv_path)
print(response)
with open("output.txt", "w") as file:
    file.write(response.text)

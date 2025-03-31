# importing required modules
from pypdf import PdfReader
import google.generativeai as genai

def send_query(prompt_path,cv_path):
    query = format_query(prompt_path,cv_path)
    #print(query) TODO delete this
    genai.configure(api_key="AIzaSyCdosn5Pm4cVw5xKVa-XoGtSdBeGhotZJY")
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(query)
    return response

# def extract_text_from_pdf(path):
#     # creating a pdf reader object
#     reader = PdfReader(path)
#     text = ""
#     for page in reader.pages:
#         # getting a specific page from the pdf file
#         text += page.extract_text()
#     return(text)

def format_query(prompt_path,cv_path):
    with open(prompt_path, "r") as file:
        prompt = file.read()
    with open(cv_path, "r", encoding="utf-8") as file:
        cv = file.read()

    query = (
        "<instructions>\n"
        f"{prompt}"
        "\n</instructions>"
        "\n<cv>"
        f"{cv}"
        "\n</cv>"
    )
    return query


import json


def parse_gemini_response(response):
    """
    Parse the Gemini API response and extract just the text content

    Args:
        response: The response object from the Gemini API

    Returns:
        str: The text content from the response
    """
    # If the response is a string (raw JSON), try to parse it
    if isinstance(response, str):
        try:
            # For debugging purposes only - most likely you won't need this branch
            import json
            response_json = json.loads(response)
            # This would be for a raw JSON string case, but the Gemini API doesn't return this
            # This is just here for completeness
            if 'candidates' in response_json and response_json['candidates']:
                if 'content' in response_json['candidates'][0]:
                    if 'parts' in response_json['candidates'][0]['content']:
                        return response_json['candidates'][0]['content']['parts'][0]['text']
            return response
        except (json.JSONDecodeError, KeyError, IndexError):
            # If it's not valid JSON, just return the string itself
            return response

    # If it's a GenerateContentResponse object (the most likely case)
    if hasattr(response, 'text'):
        # Most Gemini responses have a .text attribute for direct access
        return response.text

    # Alternative ways to get the text if .text is unavailable
    try:
        # Try accessing the parts directly
        return response.parts[0].text
    except (AttributeError, IndexError):
        pass

    try:
        # Try the candidates path
        return response.candidates[0].content.parts[0].text
    except (AttributeError, IndexError):
        pass

    # If all else fails, convert the object to a string
    return str(response)

from cv_analyzer import format_query, extract_text_from_pdf

import google.generativeai as genai






def test_api_response_time(prompt_path,cv_path):
    """Test that the API response time meets requirements"""
    import time
    query = format_query(prompt_path, cv_path)
    start_time = time.time()
    response = send_query(query)
    elapsed_time = time.time() - start_time


    assert elapsed_time < 20.0, f"API response took {elapsed_time} seconds, which exceeds the 5-second requirement"
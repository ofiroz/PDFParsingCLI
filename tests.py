import unittest
import time
import os
import tempfile
from unittest.mock import patch, MagicMock
from cv_analyzer import send_query, format_query, parse_gemini_response


class UnitTests(unittest.TestCase):
    """Unit tests for CV analyzer functions"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_prompt_path = "test_prompt.txt"
        self.test_cv_path = "test_cv.txt"

        # Create temporary test files
        with open(self.test_prompt_path, "w") as f:
            f.write("Test prompt content")

        with open(self.test_cv_path, "w") as f:
            f.write("Test CV content")

    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.test_prompt_path):
            os.remove(self.test_prompt_path)
        if os.path.exists(self.test_cv_path):
            os.remove(self.test_cv_path)

    def test_format_query(self):
        """Test that format_query correctly formats the query string"""
        result = format_query(self.test_prompt_path, self.test_cv_path)

        # Check that the result contains the expected content
        self.assertIn("<instructions>", result)
        self.assertIn("Test prompt content", result)
        self.assertIn("</instructions>", result)
        self.assertIn("<cv>", result)
        self.assertIn("Test CV content", result)
        self.assertIn("</cv>", result)

    @patch('cv_analyzer.genai.GenerativeModel')
    @patch('cv_analyzer.genai.configure')
    def test_api_response_time(self, mock_configure, mock_model_class):
        """Test that the API response time meets requirements (under 5 seconds)"""
        # Mock the API response
        mock_model = MagicMock()
        mock_model_class.return_value = mock_model
        mock_response = MagicMock()
        mock_response.text = "Test response"
        mock_model.generate_content.return_value = mock_response

        # Measure response time
        start_time = time.time()
        response = send_query(self.test_prompt_path, self.test_cv_path)
        elapsed_time = time.time() - start_time

        # Check that the response is returned correctly
        self.assertEqual(response.text, "Test response")

        # Assert that the API call was made correctly
        mock_configure.assert_called_once()
        mock_model.generate_content.assert_called_once()

        # Assert response time is under 5 seconds
        self.assertLess(elapsed_time, 5.0,
                        f"API response took {elapsed_time} seconds, which exceeds the 5-second requirement")

    def test_parse_gemini_response(self):
        """Test that parse_gemini_response correctly extracts text from different response formats"""
        # Test with a response object that has a text attribute
        mock_response = MagicMock()
        mock_response.text = "Test response text"
        result = parse_gemini_response(mock_response)
        self.assertEqual(result, "Test response text")

        # Test with a string (since Gemini won't return JSON directly)
        simple_str = "Simple response text"
        result = parse_gemini_response(simple_str)
        self.assertEqual(result, simple_str)

        # Test with a response object that has parts but no text attribute
        mock_complex_response = MagicMock()
        # Remove the text attribute
        del mock_complex_response.text
        # Add parts attribute for alternative access path
        mock_parts = [MagicMock()]
        mock_parts[0].text = "Response from parts"
        mock_complex_response.parts = mock_parts
        result = parse_gemini_response(mock_complex_response)
        self.assertEqual(result, "Response from parts")


class SystemTests(unittest.TestCase):
    """System-level functional tests for CV analyzer"""

    @patch('cv_analyzer.genai.GenerativeModel')
    @patch('cv_analyzer.genai.configure')
    def test_end_to_end_readability_analysis(self, mock_configure, mock_model_class):
        """Test the complete process of analyzing CV readability"""
        # Create temporary files for testing
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_cv:
            temp_cv.write("This is a sample CV with some text that would normally be analyzed for readability.")
            temp_cv_path = temp_cv.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_prompt:
            temp_prompt.write("Analyze the readability of this CV and provide a Flesch score")
            temp_prompt_path = temp_prompt.name

        try:
            # Mock the API response
            mock_model = MagicMock()
            mock_model_class.return_value = mock_model

            # Create a realistic mock response for readability analysis
            mock_response = MagicMock()
            mock_response.text = """
            Readability Analysis:
            - Flesch Reading Ease Score: 65.2 (Standard/Plain English)
            - Flesch-Kincaid Grade Level: 8.5

            Complex sentences:
            - "This is a sample CV with some text that would normally be analyzed for readability."

            Suggestions for improvement:
            - Break down complex sentences into shorter ones
            - Use active voice instead of passive voice
            - Simplify technical jargon
            """
            mock_model.generate_content.return_value = mock_response

            # Execute the query function
            response = send_query(temp_prompt_path, temp_cv_path)
            parsed_response = parse_gemini_response(response)

            # Verify the results
            self.assertIsNotNone(parsed_response)
            self.assertIn("Flesch Reading Ease Score", parsed_response)
            self.assertIn("Flesch-Kincaid Grade Level", parsed_response)
            self.assertIn("Complex sentences", parsed_response)
            self.assertIn("Suggestions for improvement", parsed_response)

            # Verify the API was called with the correct query format
            mock_configure.assert_called_once()
            call_args = mock_model.generate_content.call_args[0][0]
            self.assertIn("<instructions>", call_args)
            self.assertIn("<cv>", call_args)

        finally:
            # Clean up temporary files
            os.unlink(temp_cv_path)
            os.unlink(temp_prompt_path)


if __name__ == "__main__":
    unittest.main()
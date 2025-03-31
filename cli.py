import argparse
import os
from PyPDF2 import PdfReader

from cv_analyzer import send_query


class PDFProcessor:
    def __init__(self):
        self.extracted_text = ""
        self.output_file = "extracted_text.txt"
        self.version = "1.0.1"
    
    def display_welcome(self):
        print("="*50)
        print("      Welcome to PDF Text Processor      ")
        print("="*50)
        print("This application extracts text from PDF cv files")
        print("and provides readability analysis")        
        print("="*50)

    def display_help(self):
        """Display help information about available commands."""
        print("\nAvailable commands:")
        print("--file [path]   : Upload and process a new PDF file.")
        print("-s | --score    : Flesch-Score, a readability metric (0-30: hard, 60-70: standard, 90-100: easy).")
        print("-g | --grade    : Flesch-Kincaid Grade Level, retuens the text U.S. school grade level (e.g., score 8 means 8th-grade reading level).")
        print("-i | --improve  : Suggests improvements to make the text easier to read.")
        print("-v | --version  : Returns this app version.")
        print("-h | --help     : Display this help information.")
        print("exit            : Exit application.")
        print("\nAfter processing, you can enter these commands directly.")

    def extract_text(self, pdf_path=None):
        """Extract text from a PDF file and save it to a text file."""
        while True:
            try:
                # If no path provided, prompt the user
                if pdf_path is None or pdf_path.strip() == "":
                    pdf_path = input("Please enter the path to the PDF file: ").strip()
                
                # Check if file exists
                if not os.path.exists(pdf_path):
                    print(f"Error: File '{pdf_path}' not found.\n")
                    pdf_path = None
                    continue
                
                # Check if file is a PDF
                if not pdf_path.lower().endswith('.pdf'):
                    print(f"Error: File '{pdf_path}' is not a PDF file.\n")
                    pdf_path = None
                    continue
                
                # Extract text from PDF
                print(f"Processing file: {pdf_path}")
                reader = PdfReader(pdf_path)
                self.extracted_text = ""
                
                for page in reader.pages:
                    self.extracted_text += page.extract_text()
                
                with open(self.output_file, 'w', encoding='utf-8') as f:
                    f.write(self.extracted_text)
                
                print("Done")
                return True
            
            except Exception as e:
                print(f"Error processing PDF: {str(e)}")
                pdf_path = None
        
    def interactive_mode(self):
        global path
        print("\nEnter a command (--help for options, or 'exit' to quit):")
        while True:
            command = input("> ").strip().lower()
            if command == 'exit':
                print("Exiting application. Goodbye!")
                break
            elif command in ['--help', '-h']:
                self.display_help()
            elif command in ['--version', '-v']:
                print(self.version)
            elif command in ['--score', '-s']:
                if path is None:
                    print("Error: Please enter a path to a PDF file.")
                else:
                    answer = send_query("prompts/readability score prompt.txt",path)
                pass
            elif command in ['--grade', '-g']:
                if path is None:
                    print("Error: Please enter a path to a PDF file.")
                else:
                    answer = send_query("prompts/Flesch grade prompt.txt", path)
                pass
            elif command in ['--complexity', '-g']:
                if path is None:
                    print("Error: Please enter a path to a PDF file.")
                else:
                    answer = send_query("prompts/complexity analysis.txt", path)
                pass
            elif command in ['--improve', '-i']:
                if path is None:
                    print("Error: Please enter a path to a PDF file.")
                else:
                    answer = send_query("prompts/improvement suggestions prompt.txt", path)
                pass
            elif command.startswith('--file'):
                parts = command.split(maxsplit=1)
                path = parts[1] if len(parts) == 2 else None
                self.extract_text(path)
            else:
                print(f"Unknown command: {command}")
                print("Use --help to see available commands.")
    
def main():
    processor = PDFProcessor()
    
    processor.display_welcome()
    
    processor.extract_text()
    processor.interactive_mode()

if __name__ == "__main__":
    main()
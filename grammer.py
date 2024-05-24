import fitz  # PyMuPDF
from termcolor import colored
import tempfile
import os
import language_tool_python
 
class Grammer_checker():
    @staticmethod
    def extract_text_from_pdf(pdf_path):
        doc = fitz.open(pdf_path)
        text = ""
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text()
 
        doc.close()
        return text
 
    @staticmethod
    def error_correcting(text):
        tool = language_tool_python.LanguageTool('en-US')
        datasets = tool.correct(text)
        return datasets
 
    @staticmethod
    def highlight_mistakes(original_text, corrected_text):
        original_lines = original_text.splitlines()
        corrected_lines = corrected_text.splitlines()
 
        highlighted_text = ""
 
        for original_line, corrected_line in zip(original_lines, corrected_lines):
            original_words = original_line.split()
            corrected_words = corrected_line.split()
 
            for original, corrected in zip(original_words, corrected_words):
                if original != corrected:
                    highlighted_text += colored(corrected, 'green') + ' '
                else:
                    highlighted_text += original + ' '
 
            highlighted_text += '\n'  # Add a newline after each line
           
 
        return highlighted_text
 
    @staticmethod
    def main():
        # Replace 'your_file.pdf' with the actual path to your PDF file
        pdf_path = 'backend\\uploads\\India_is_a_dierse_and_culurally_rich_country_located_in_South_Asia.pdf'
 
        # Extract text from the PDF
        original_text = Grammer_checker.extract_text_from_pdf(pdf_path)
 
        # Perform spelling and grammar correction
        corrected_data = Grammer_checker.error_correcting(original_text)
 
        # Highlight mistakes
        print(Grammer_checker.highlight_mistakes(original_text, corrected_data))
 
 
if __name__ == "__main__":
    Grammer_checker.main()
 

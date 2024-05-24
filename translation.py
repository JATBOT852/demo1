from googletrans import Translator
from PyPDF2 import PdfReader
import cv2
import pytesseract
from gtts import gTTS
from googletrans import Translator
from docx import Document
from io import BytesIO
from PyPDF2 import PdfReader
import textwrap
from fpdf import FPDF

class TranslationFile:
    @staticmethod
    def extract_text_from_image(scanned_image):
        gray_image = cv2.cvtColor(scanned_image, cv2.COLOR_RGB2GRAY)
        text = pytesseract.image_to_string(gray_image)
        print("Extracted Text from Image:")
        print(text)
        return text
    @staticmethod
    def extract_text_from_pdf(pdf_path):
        with  open(pdf_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
            print("Extracted Text from PDF:")
            
            
            return text
        
        
    @staticmethod
    def extract_text_from_text_file(text_file_path):
        with open(text_file_path, 'r') as file:
            text = file.read()
            print("Text from Text File:")
            print(text)
            return text
    @staticmethod
    def extract_text_from_word_document(docx_path):
        doc = Document(docx_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + '\n'
        print("Text from Word Document:")
        print(text)
        return text
    @staticmethod
    @staticmethod
    def translate_text(text,  target_language):
        translator = Translator()

        # Check if text is None or empty
        if not text:
            print("Error: Empty or None text provided for translation.")
            return ""

        try:
            translator.raise_Exception = True
            translation = translator.translate(text, src="auto", dest=target_language)
            translated_text = translation.text
            return translated_text
        except Exception as e:
            print(f"Error during translation: {e}")
            return ""
    

    @staticmethod
    def chunk_and_translate(text, chunk_size ,target_language):
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

        translated_chunks = []
        for chunk in chunks:
            translated_chunk = TranslationFile.translate_text(chunk, target_language)
            translated_chunks.append(translated_chunk)

        return ''.join(translated_chunks)
    @staticmethod
    def text_to_pdf(text, filename="translated_text.pdf"):
        a4_width_mm = 210
        pt_to_mm = 0.35
        fontsize_pt = 10
        fontsize_mm = fontsize_pt * pt_to_mm
        margin_bottom_mm = 10
        character_width_mm = 7 * pt_to_mm
        width_text = a4_width_mm / character_width_mm

        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.set_auto_page_break(True, margin=margin_bottom_mm)
        pdf.add_page()
        pdf.set_font(family='Courier', size=fontsize_pt)
        splitted = text.split('\n')

        for line in splitted:
            lines = textwrap.wrap(line, width_text)

            if len(lines) == 0:
                pdf.ln()

            for wrap in lines:
                translated_line =wrap  # Translate English to Telugu
                pdf.cell(0, fontsize_mm, translated_line.encode('latin-1', 'replace').decode('latin-1'), ln=1)

        pdf.output(filename, 'F')
        return filename
 

if __name__ == "__main__":
    Translation=TranslationFile()
    path="CBN Sir Bail Judgemet Copy.pdf"
    text=Translation.extract_text_from_pdf(path)
    src_lange="en"
    tartgetlanguage="te"
    chunk_size=4500
    trans=Translation.chunk_and_translate(text,chunk_size,src_lange, tartgetlanguage)
    output_file="summarized_text.pdf"
    pdf=Translation.text_to_pdf(trans, filename="translated_text.pdf")
    print(text)
    print(trans)
    print(pdf)


    


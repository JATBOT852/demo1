from googletrans import Translator
from PyPDF2 import PdfReader
import cv2
import pytesseract
from gtts import gTTS
from googletrans import Translator
from docx import Document
from io import BytesIO
from PyPDF2 import PdfReader
from gtts import gTTS
from io import BytesIO

class Audiblity:
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
    def translate_text(text, target_language):
        translator = Translator()

        try:
            translation = translator.translate(text, dest=target_language)
            translated_text = translation.text
            return translated_text
        except Exception as e:
            print(f"Translation error: {e}")
            return None


    @staticmethod
    def chunk_and_translate(text, chunk_size, target_language):
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

        translated_chunks = []
        for chunk in chunks:
            translated_chunk = Audiblity.translate_text(chunk, target_language)
            translated_chunks.append(translated_chunk)

        return ''.join(translated_chunks)
    @staticmethod
    def text_to_speech(text, target_language):
        if text:
            tts = gTTS(text=text, lang=target_language, slow=False)
            audio_buffer = BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_data = audio_buffer.getvalue()
            return audio_data
        else:
            # Handle the case where no text is provided
            print("No text provided for speech synthesis.")
            return None

if __name__ == "__main__":
    audio=Audiblity()
    pdf="CBN Sir Bail Judgemet Copy.pdf"
    text=audio.extract_text_from_pdf(pdf)
    chunk_size=3000
    target_language="te"

    trans=audio.chunk_and_translate(text,chunk_size,target_language)
    print(trans)
    audio=audio.text_to_speech(text, target_language)
    print(audio)
    


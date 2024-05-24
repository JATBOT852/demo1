
from PyPDF2 import PdfReader
import cv2
import pytesseract
from fpdf import FPDF
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from docx import Document
import textwrap
import nltk
import spacy
import io
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
import cv2
import pytesseract
from PyPDF2 import PdfReader
from docx import Document
from PyPDF2 import PdfReader
import cv2
import pytesseract
from fpdf import FPDF
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from docx import Document
import textwrap


#DATE:10/01/2024
#Implement logic to handle text input from different sources (file upload, manual entry, camera capture).
#Integrate libraries for file handling and OCR for camera input.
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR"
class TextProcessor:

    @staticmethod
    def extract_text_from_image(scanned_image_path):
    # Load the image using OpenCV
        scanned_image = cv2.imread(scanned_image_path)
        
        # Check if the image is loaded properly
        if scanned_image is None:
            print("Error: Unable to load image.")
            return None
        
        # Convert the image to grayscale
        gray_image = cv2.cvtColor(scanned_image, cv2.COLOR_BGR2GRAY)
        
        # Perform OCR using Tesseract
        text = pytesseract.image_to_string(gray_image)
        
        # Print the extracted text
        print("Extracted Text from Image:")
        print(text)
        
        # Return the extracted text
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
            return text

    @staticmethod
    def extract_text_from_word_document(docx_path):
        doc = Document(docx_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + '\n'
        print("Text from Word Document:")
        return text
    @staticmethod
    def get_sentences_count(text, summary_length):
        sentences_text = len(nltk.sent_tokenize(text))
        sent = []
        if summary_length == "Very_Short":
            sentences_count = max(1, round(0.10 * sentences_text))
            sent.append(sentences_count)
        elif summary_length == "Short":
            sentences_count = max(1, round(0.35 * sentences_text))
            sent.append(sentences_count)
        elif summary_length == "Medium":
            sentences_count = max(1, round(0.55 * sentences_text))
            sent.append(sentences_count)
        elif summary_length == "Long":
            sentences_count = max(1, round(0.80 * sentences_text))
            sent.append(sentences_count)
        else:
            print('Invalid option')

        return int(sent[0]) if sent else 0

    @staticmethod
    def summarize_text_sumy(text, sentences_count):
        
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, sentences_count=sentences_count)
        summary_text = " ".join(str(sentence) for sentence in summary)
        #print("Summary:")
        return summary_text
    @staticmethod
    def text_to_pdf(text, filename="summarized_text.pdf"):
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
                pdf.cell(0, fontsize_mm, wrap.encode('latin-1', 'replace').decode('latin-1'), ln=1)

        pdf.output(filename, 'F')
        return filename

    @staticmethod
    def text_in_words_and_sentences(text):
        # Count words
        words = text.split()
        num_words = len(words)
        

        # Count sentences using nltk
        sentences = nltk.sent_tokenize(text)
        num_sentences = len(sentences)

        #print(f"Number of words in the text: {num_words}")
        #print(f"Number of sentences in the text: {num_sentences}")

        return num_words, num_sentences
#Date:11/01/2024
#Genaarte the key words from extracted text
    @staticmethod
    def extracted_text_words(text, num_keywords=5):
        if not text:
            print("Input text is empty.")
            return []   
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)

        # Tokenize the text and extract lemmatized tokens
        tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]

        # Convert tokens back to a sentence
        preprocessed_text = ' '.join(tokens)

        # Use TF-IDF to extract the top keywords
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform([preprocessed_text])

        # Get feature names and corresponding TF-IDF scores
        feature_names = vectorizer.get_feature_names_out()
        tfidf_scores = X.toarray()[0]

        # Create a list of (word, TF-IDF score) tuples
        word_tfidf_tuples = list(zip(feature_names, tfidf_scores))

        # Sort the tuples by TF-IDF score in descending order
        sorted_word_tfidf = sorted(word_tfidf_tuples, key=lambda x: x[1], reverse=True)

        # Extract the top N keywords
        top_keywords = [word for word, _ in sorted_word_tfidf[:num_keywords]]

        return top_keywords
#summarize the genarated text based key words 
    @staticmethod
    def summarize_content(text, selected_keywords):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)

        # Extract sentences containing selected keywords
        relevant_sentences = [sent.text for sent in doc.sents if any(keyword.lower() in sent.text.lower() for keyword in selected_keywords)]

        # Join relevant sentences to create the summary
        summary = ' '.join(relevant_sentences)

        return summary
    @staticmethod               
    def calculate_reduction_percentages(extracted_text_words, extracted_text_sentences, summary_text_words, summary_text_sentences):
    # Calculate reduction
        reduce_word = extracted_text_words - summary_text_words
        reduce_sentence = extracted_text_sentences - summary_text_sentences

        # Calculate reduction percentages
        reduction_percentage_words = (reduce_word / extracted_text_words) * 100
        reduction_percentage_sentences = (reduce_sentence / extracted_text_sentences) * 100

        # Store print statements in variables
        
        sentence_reduction_info = f"{reduction_percentage_sentences:.0f}%"

        # Return a dictionary with the print statements
        return sentence_reduction_info

#make bullet points
    @staticmethod

    def create_bullet_points(text):
    # Load spaCy model
    
            nlp = spacy.load("en_core_web_sm")

            # Process the text using spaCy
            doc = nlp(text)

            # Check if the processed text is not empty
            if len(doc) == 0:
                return "No content to summarize."

            # Convert generator to a list of sentences
            sentences = list(doc.sents)

            # Combine every 3 lines as one sentence
            combined_sentences = [" ".join([sent.text.strip() for sent in sentences[i:i + 4]]) for i in
                                range(0, len(sentences), 4)]

            # Create bullet points
            bullet_points = ['\u2022' + sentence for sentence in combined_sentences]
            return  "\n".join(bullet_points)
    @staticmethod
    def combined_sentences(text):
        text=processor.extract_text_from_pdf(text)
        paragraphs = text.split("\n")
        
        # Combine paragraphs with proper sentence continuity
        bullet_points = []
        current_bullet = []
        for paragraph in paragraphs:
            # If the paragraph is not empty and starts with "number.", start a new bullet point
            stripped_paragraph = paragraph.strip()
            if stripped_paragraph and stripped_paragraph.endswith(".") and stripped_paragraph[:-1].isdigit():
                if current_bullet:
                    bullet_points.append(" ".join(current_bullet))
                current_bullet = [stripped_paragraph]
            else:
                # Add the paragraph to the current bullet point
                current_bullet.append(stripped_paragraph)
        
        # Add the last bullet point
        if current_bullet:
            bullet_points.append(" ".join(current_bullet))
        
        # Join bullet points with newlines
        bullet_point= "\n".join("" + bp for bp in bullet_points)
        return bullet_point    

       



       
if __name__ == "__main__":
    processor = TextProcessor()
    pdf="Backend\\uploads\\CBN_Sir_Bail_Judgemet_Copy.pdf"
    text=TextProcessor.extract_text_from_pdf(pdf)
    print(text)
    key=TextProcessor.extracted_text_words(text, num_keywords=5)
    print(key)
    keyword=input('enter keyword')
    et=TextProcessor.summarize_content(text, keyword)
    summary=TextProcessor.summarize_text_sumy(et, sentences_count=5)
    print(et)

       


 

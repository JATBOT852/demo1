from flask import Flask, redirect, url_for, session, request,render_template
from flask import Flask, request, jsonify, session, redirect
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from flask_cors import CORS
import smtplib
from flask_mail import *  
from random import *  
from random import randint
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
from docx import Document
from summarization2 import TextProcessor
from translation import TranslationFile
from audiblity import Audiblity
import base64
from grammer import Grammer_checker
from gtts import gTTS
from io import BytesIO
from voicetyping import Spell_Checker
import fitz
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
app = Flask(__name__)
app.secret_key = '21124105752157'
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    reset_token = db.Column(db.String(100), unique=True)
 
    def __init__(self, email, password, name):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.reset_token = None
 
    def check_password(self, password):
        try:
            if self.password and password:
                return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
            else:
                return False
        except ValueError as e:
            print("Error checking password:", e)
            return ("Falsehecking password:", e)
                
 
with app.app_context():
    db.create_all()
    users = User.query.all()
    for user in users:
        print(user.name,user.email,user.reset_token )

otp = randint(000000,999999)  
def send_email(receiver_email, otp):
    sender_email = "mvprasannakumar6301@gmail.com"
    password = "mfqa ykdz zlrb ufwc"
 
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    name="JATBOT_USER"
    subject = "OTP verification using Python"
    body = f"Dear {name},\n\nYour OTP is {otp}."
    message = f"Subject: {subject}\n\n{body}"
 
    server.sendmail(sender_email, receiver_email, message)
    server.quit()
def send_message_to_email(sender_email, receiver_email, message,name,email):
    smtp_server = "smtp.gmail.com"
    port = 587
    smtp_username = sender_email
    smtp_password =  "mfqa ykdz zlrb ufwc"
 
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    name=name
    email=email
    msg['Subject'] = f"Complaint from {name}&{email}"
    body = message
    msg.attach(MIMEText(body, 'plain'))
 
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)
    server.quit()

#AI ENGINE CODE
extracted_text = ""
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def text_to_speech(text, target_language):
    try:
        if text:
            tts = gTTS(text=text, lang=target_language, slow=False)
            audio_buffer = BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_data = audio_buffer.getvalue()
            return audio_data
        else:
            return None  # Return None if no text is provided
    except Exception as e:
        print(f"Error in text_to_speech: {e}")
        return None
def extract_text_from_pdf(pdf_path):
        doc = fitz.open(pdf_path)
        text = ""
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text()
 
        doc.close()
        return text
def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text


@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        print(email)
        password = data.get('password')

        # Check if the email already exists
        existing_user = User.query.filter_by(email=email).first()
        print(existing_user)
        if existing_user:
            return jsonify({'error': 'Email already exists'}), 400

        if name and email and password:
            new_user = User(name=name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'User registered successfully'}), 201
        else:
            return jsonify({'error': 'Name, email, and password are required'}), 400
    elif request.method == 'GET':
        return jsonify({"message": "ok"})
    
@app.route('/signin', methods=['POST','GET'])
def signin():
    if request.method=="POST":
        email = request.json['email']
        password = request.json['password']
       
        user = User.query.filter_by(email=email).first()
        

        if user and user.check_password(password):
            return jsonify({'name': user.name, 'message': 'Login successful'}), 200
        else:
            return jsonify(error="Invalid credentials"), 401
    elif request.method=='GET':
        return jsonify({"message": "ok"})

@app.route('/forget_password', methods=['POST', 'GET'])
def forget_password():
    if request.method == 'POST':
        rec_email = request.json.get('email')
        if not rec_email:
            return jsonify({'error': 'Email is required.'}), 400
        send_email(rec_email, otp)
        return jsonify({'message': 'OTP sent successfully.'}), 200
    elif request.method == 'GET':
        return jsonify({'error': 'Method not allowed.'}), 405
    else:
        return jsonify({'error': 'Method not allowed.'}), 405
@app.route('/verify_otp', methods=['POST','GET'])
def verify_otp():
    if request.method == 'POST':
        data = request.json
        user_otp = data.get('otp')
        print("User OTP:", user_otp)  # Debugging message
        if otp == int(user_otp): 
             return jsonify({'message': 'OTP verified successfully.'}), 200
        else:
            return jsonify({'error': 'Invalid OTP. Please enter the correct OTP.'}), 400
    elif request.method == 'POST':
        return jsonify({"message": "ok"})
@app.route("/resetpassword", methods=['POST', 'GET'])
def reset_password():
    if request.method == 'POST':
        data = request.json
        
        if not data:
            return jsonify({'error': 'No JSON data provided.'}), 400

        email = data.get('email')
        print(email)
        password = data.get('password')
        print(password)
        confirm_password = data.get('confirm_password')
        print(confirm_password)
        
        if not email or not password or not confirm_password:
            return jsonify({'error': 'Email, password, and confirm_password are required.'}), 400
        
        if password != confirm_password:
            return jsonify({'error': 'Passwords do not match. Please try again.'}), 400

        # Hash the new password before updating it in the database

        # Update user's password in the database with the hashed password
        user = User.query.filter_by(email=email).first()
        if user is None:
            return jsonify({'error': 'User not found.'}), 404
        
        user.password = password  # Update the password
        print(user.password)
        db.session.commit()
        
        return jsonify({'message': 'Password reset successfully.'}), 200
    
    elif request.method == 'GET':
        return jsonify({'message': 'Enter your new password to reset.'}), 200
    
    else:
        return jsonify({'error': 'Method not allowed.'}), 405
@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(os.path.abspath(app.config['UPLOAD_FOLDER']), filename)
            file.save(filepath)

            # Extract text based on file type
            if filename.endswith(".pdf"):
                extracted_text = TextProcessor.extract_text_from_pdf(filepath)
            elif filename.endswith(".docx"):
                extracted_text = TextProcessor.extract_text_from_word_document(filepath)
            elif filename.endswith(".txt"):
                extracted_text = TextProcessor.extract_text_from_text_file(filepath)
            elif filename.endswith((".png", ".jpg", ".jpeg")):
                extracted_text = TextProcessor.extract_text_from_image(filepath)
            else:
                print(f"Unsupported file format: {filename}")
                return jsonify({'error': 'Unsupported file format'})

            # Perform text analysis
            num_word, num_sent = TextProcessor.text_in_words_and_sentences(extracted_text)
            keywords = TextProcessor.extracted_text_words(extracted_text, num_keywords=5)

            result = ",".join(keywords)

            user = request.args.get('type')
            sent_number = int(request.args.get('sent_number', 5))

            if user == "paragraph":
                summary = TextProcessor.summarize_text_sumy(extracted_text, sent_number)
                summary_num_word, summary_num_sent = TextProcessor.text_in_words_and_sentences(summary)
                sentence_reduction_info = TextProcessor.calculate_reduction_percentages(num_sent, num_word, summary_num_sent, summary_num_word)
                return jsonify({'text': summary, "Rnum_word": summary_num_word, "Rnum_sent": summary_num_sent, 'statistics': sentence_reduction_info})

            elif user == "bulletpoints":
                summary_length = request.args.get('summary_length')
                sentences_count = TextProcessor.get_sentences_count(extracted_text, summary_length)
                summary = TextProcessor.summarize_text_sumy(extracted_text, sentences_count)
                bullet_summary = TextProcessor.create_bullet_points(summary)
                summary_text_words, summary_text_sentences = TextProcessor.text_in_words_and_sentences(bullet_summary)
                sentence_reduction_info = TextProcessor.calculate_reduction_percentages(num_word, num_sent, summary_text_words, summary_text_sentences)
                return jsonify({'text': bullet_summary, "Bnum_word": summary_text_words, "Bnum_sent": summary_text_sentences, 'statistics':  sentence_reduction_info})

            elif user == "keywords":
                selected_keywords = request.args.get('selected_keyword')  # Corrected variable name
                if selected_keywords is not None:  # Check if selected_keywords is not None
                    sent_number = int(request.args.get('sent_number', 0))  # Corrected variable name and converted to int
                    selected_keywords = [keyword.strip() for keyword in selected_keywords.split(',')]
                    selected_keyword_summary = TextProcessor.summarize_content(extracted_text, selected_keywords)
                    selected_keyword_summary = TextProcessor.summarize_text_sumy(selected_keyword_summary, sent_number)
                    summary_text_words, summary_text_sentences = TextProcessor.text_in_words_and_sentences(selected_keyword_summary)
                    sentence_reduction_info = TextProcessor.calculate_reduction_percentages(num_word, num_sent, summary_text_words, summary_text_sentences)
                    return jsonify({'keyword_summary': selected_keyword_summary, 'num_word': summary_text_words, 'num_sent': summary_text_sentences,'statistics':  sentence_reduction_info})
                else:
                    return jsonify({'error': 'Invalid'})
            return jsonify({'text': extracted_text, "Lnum_word": num_word, "Lnum_sent": num_sent, 'keywords': result})

        else:
            return jsonify({'error': 'Invalid file'})

    elif request.method == 'GET':
        # Handle GET request
        return jsonify({'message': 'GET request received'})

@app.route('/translate', methods=['GET', 'POST'])
def translate():
    if request.method == 'POST':
        source_language = request.form.get('source_language')
        target_language = request.form.get('target_language')
       
        manual_text = request.form.get('manual_text')  # Get manual text input
       
        if not manual_text and 'file' not in request.files:
            return jsonify({'error': 'No text or file provided'})
 
        if manual_text:
            extracted_text = manual_text  # Use manual text input
        else:
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No selected file'})
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(os.path.abspath(app.config['UPLOAD_FOLDER']), filename)
                file.save(filepath)
               
                if filename.endswith(".pdf"):
                    extracted_text = TextProcessor.extract_text_from_pdf(filepath)
                elif filename.endswith(".docx"):
                    extracted_text = extract_text_from_docx(filepath)
                elif filename.endswith(".txt"):
                    extracted_text = TextProcessor.extract_text_from_text_file(filepath)
                elif filename.endswith((".png", ".jpg", ".jpeg")):
                    extracted_text = TextProcessor.extract_text_from_image(filepath)
                else:
                    return jsonify({'error': 'Invalid file format'})
            else:
                return jsonify({'error': 'Invalid file format'})
       
        chunk_size = 4500
        translated_text = TranslationFile.chunk_and_translate(extracted_text, chunk_size, target_language)
        return jsonify({'original_text': extracted_text, 'translated_text': translated_text})
 
    elif request.method == 'GET':
        # Handle GET request
        return jsonify({'message': 'GET request received'})

@app.route('/audiblity', methods=['GET','POST']) 
def audiblity():
    if request.method == 'POST':
        source_language = request.form.get('source_language')
        target_language = request.form.get('target_language')
       
        manual_text = request.form.get('manual_text')  # Get manual text input
       
        if not manual_text and 'file' not in request.files:
            return jsonify({'error': 'No text or file provided'})
 
        if manual_text:
            extracted_text = manual_text  # Use manual text input
        else:
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No selected file'})
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(os.path.abspath(app.config['UPLOAD_FOLDER']), filename)
                file.save(filepath)
               
                if filename.endswith(".pdf"):
                    extracted_text = TextProcessor.extract_text_from_pdf(filepath)
                elif filename.endswith(".docx"):
                    extracted_text = extract_text_from_docx(filepath)
                elif filename.endswith(".txt"):
                    extracted_text = TextProcessor.extract_text_from_text_file(filepath)
                elif filename.endswith((".png", ".jpg", ".jpeg")):
                    extracted_text = TextProcessor.extract_text_from_image(filepath)
                else:
                    return jsonify({'error': 'Invalid file format'})
            else:
                return jsonify({'error': 'Invalid file format'})
       
            chunk_size = 4500
            translated_text = TranslationFile.chunk_and_translate(extracted_text, chunk_size, target_language)
            audio = Audiblity.text_to_speech(translated_text, target_language)
 
            # Convert audio to base64
            if audio:
                audio_base64 = base64.b64encode(audio).decode('utf-8')
            else:
                audio_base64 = ''
 
            return jsonify({'original_text': extracted_text, 'translated_text': translated_text, 'audio': audio_base64})
    elif request.method == 'GET':
        # Handle GET request
        return jsonify({'message': 'GET request received'})

        
@app.route('/Grammer_Checker', methods=['GET','POST'])
def Grammer_Checker():
    if request.method == 'POST':
        # Check if file is uploaded
        manual_text = request.form.get('manual_text')  # Get manual text input
       
        if not manual_text and 'file' not in request.files:
            return jsonify({'error': 'No text or file provided'})

        if manual_text:
            extracted_text = manual_text  # Use manual text input
        else:
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No selected file'})
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(os.path.abspath(app.config['UPLOAD_FOLDER']), filename)
                file.save(filepath)
               
                if filename.endswith(".pdf"):
                    extracted_text = extract_text_from_pdf(filepath)
                elif filename.endswith(".docx"):
                    extracted_text = extract_text_from_docx(filepath)
                elif filename.endswith(".txt"):
                    extracted_text = TextProcessor.extract_text_from_text_file(filepath)
                elif filename.endswith((".png", ".jpg", ".jpeg")):
                    extracted_text = TextProcessor.extract_text_from_image(filepath)
                else:
                    return jsonify({'error': 'Invalid file format'})
            else:
                return jsonify({'error': 'Invalid file format'})

        # Perform grammar checking
        corrected = Grammer_checker.error_correcting(extracted_text)
        corrected_text = Grammer_checker.highlight_mistakes(extracted_text, corrected) 

        return jsonify({"original_text": extracted_text, "corrected_sentences": corrected_text})

    elif request.method == 'GET':
        # Handle GET request
        return jsonify({'message': 'GET request received'})

@app.route('/suggest-corrections', methods=['POST','GET'])
def check_text():
    if request.method=="POST":
        data = request.get_json()
        text = data.get('text', '')
        corrections = Spell_Checker.suggest_corrections(text)
        synonyms = {word: Spell_Checker.get_synonyms(word) for word in corrections}
        return jsonify({'corrections': corrections})
    elif request.method=="GET" :
       return jsonify({'massage':"ok"})
@app.route('/send_complaint', methods=['POST'])
def send_complaint():
    try:
        data = request.get_json()
        sender_email = "mvprasannakumar6301@gmail.com"
        receiver_email = "jatbot36@gmail.com"
        message = data['message']
        name= data['name']
        email=data['email']
        print(name)
        print(email)
        print(message)
       
        send_message_to_email(sender_email, receiver_email, message,name,email)
        return jsonify({"message": "Complaint sent successfully!"})
    except Exception as e:
        print(e)  # Print out the error message
        return jsonify({"error": "Internal Server Error"}), 500


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    app.run(host="0.0.0.0",port=8000)

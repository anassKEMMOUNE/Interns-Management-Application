import os
from docx import Document
import mammoth
import PyPDF2  
from PIL import Image
import pytesseract
import re
import nltk
import unidecode
from docx2pdf import convert
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')





def preprocess_text(text):
    # Remove special characters, URLs, and mentions
    text = re.sub(r'http\S+|www\S+|@+', '', text)
    
    # Keep French characters with accents
    text = re.sub(r'[^a-zA-ZÀ-ÿ\s]', '', text)
    
    return text.lower()

def tokenize_and_lemmatize(text):
    tokens = nltk.word_tokenize(text)
    lemmatizer = nltk.WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return lemmatized_tokens

def pdf_to_text(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()

        text =  preprocess_text(text)
        text = unidecode.unidecode(text)
        text1 = tokenize_and_lemmatize(text)
        return {"tokenized"  :text1 , "untokenized": re.sub(r"\s+", "", text, flags=re.UNICODE)}



# print(pdf_to_text("Resumes/anasscv.pdf")["tokenized"])
# print("__________________________________________________")
# print(pdf_to_text("Resumes/anasscv.pdf")["untokenized"])


def image_to_text(image_path):
    # Open the image using Pillow
    img = Image.open(image_path)

    # Perform OCR on the image
    text = pytesseract.image_to_string(img)

    text =  preprocess_text(text)
    text = unidecode.unidecode(text)
    text1 = tokenize_and_lemmatize(text)
    return {"tokenized"  :text1 , "untokenized": re.sub(r"\s+", "", text, flags=re.UNICODE)}


# image_path = 'Resumes/anass.png'
# result_text = image_to_text(image_path)

# print(result_text["tokenized"])
# print("__________________________________________________")
# print(result_text["untokenized"])

def docx_to_text(docx_path) :
    with open(docx_path, "rb") as docx_file:
        result = mammoth.extract_raw_text(docx_file)
        text = result.value # The raw text
        messages = result.messages
        print("docx to text messages : ",messages)

        text =  preprocess_text(text)
        text = unidecode.unidecode(text)
        text1 = tokenize_and_lemmatize(text)
        return {"tokenized"  :text1 , "untokenized": re.sub(r"\s+", "", text, flags=re.UNICODE)}
    

# docx_path = 'Resumes/cv.docx'
# result_text = docx_to_text(docx_path)

# print(result_text["tokenized"])
# print("__________________________________________________")
# print(result_text["untokenized"])


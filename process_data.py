import fitz 
import re

# Changing Pdf to txt(string)
def pdf_to_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ''
    for page in doc:
        text += page.get_text()
    return text

# Cleaning text
def clean_text(text):
    # Removing newline characters
    text = text.replace('\n', ' ')
    # Removing extra spaces
    text = re.sub(' +', ' ', text)
    return text

# Saving Cleaned text
def save_text(file_path, text):
    with open(file_path, "w") as f:
        f.write(text)

def main():
    pdf_path = '/content/drive/MyDrive/2023-record-and-fact-book.pdf'
    # Convert PDF to text
    text = pdf_to_text(pdf_path)

    # Cleaning text
    cleaned_text = clean_text(text)

    # Saving Cleaned text to a new file
    save_text("/content/drive/MyDrive/record_fact.txt", cleaned_text)

if __name__ == "__main__":
    main()

import PyPDF2
import os

TEXT_FILES_DIRECTORY = "text_files/"

def get_file_size(file):
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    return size

def extract_text_and_create_text_file(pdf_file, text_filename):
    text = ''
    pdf_file.seek(0)
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    with open(os.path.join(TEXT_FILES_DIRECTORY, text_filename), 'w', encoding='utf-8') as text_file:
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:  # Check if text is not None
                text_file.write(page_text + '\n')
    pdf_file.seek(0)  # Reset the PDF file position if needed

def upload_file(file, filename):
    file_size = get_file_size(file)
    text_filename = f"{os.path.splitext(filename)[0]}.txt"
    extract_text_and_create_text_file(file, text_filename)
    
    file_details = {
        "Filename": filename,
        "File size": file_size,
        "Text File": os.path.join(TEXT_FILES_DIRECTORY, text_filename)
    }
    
    confirmation_message = f"File '{filename}' processed successfully and saved as '{text_filename}' in the specified directory."
    return {"message": confirmation_message, "file_details": file_details}

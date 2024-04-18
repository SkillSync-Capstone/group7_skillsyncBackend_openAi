import os
import boto3
import PyPDF2
from io import BytesIO

def get_file_size(file):
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    return size

def upload_text_to_s3(pdf_file, filename, bucket_name):
    pdf_file.seek(0)
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text_content = ''
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text_content += page_text + '\n'

    # Create a S3 client
    s3 = boto3.client('s3')
    object_name = f"text_files/{filename}.txt"
    # Upload the file
    s3.put_object(Body=text_content, Bucket=bucket_name, Key=object_name)
    return f"File uploaded to S3 with key {object_name}"

def upload_file(file, filename, bucket_name):
    
    # Check the split operation
    base_filename = os.path.splitext(filename)[0]
    
    file_size = get_file_size(file)
    
    # Ensure this function is properly handling its inputs
    confirmation_message = upload_text_to_s3(file, base_filename, bucket_name)
    
    # Check final URI formation
    s3_uri = f"s3://{bucket_name}/text_files/{base_filename}.txt"
    
    file_details = {
        "Filename": filename,
        "File size": file_size,
        "S3 URI": s3_uri
    }
    
    return {"message": confirmation_message, "file_details": file_details}
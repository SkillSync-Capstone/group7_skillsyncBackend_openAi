from flask import Blueprint, request, jsonify
from services.pdf_service import upload_file
from services.query_service import handle_new_query

api_routes = Blueprint('api_routes', __name__)

Bucket="cyclic-plum-cautious-woodpecker-ap-southeast-2",

@api_routes.route('/process_new_pdf', methods=['POST'])
def pdf_new_api():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF file provided'}), 400
    pdf_file = request.files['pdf']
    filename = pdf_file.filename
    if not filename.endswith('.pdf'):
        return jsonify({"error": "File is not a PDF."}), 400
    
    try:
        result = upload_file(pdf_file, filename,"cyclic-plum-cautious-woodpecker-ap-southeast-2" )  
        return jsonify(result)
    except Exception as e:
        # Log the error and provide a user-friendly message
        print(f"An error occurred: {str(e)}")
        return jsonify({'error': 'Failed to process file'}), 500

@api_routes.route('/handle_new_query', methods=['POST'])
def query_new_api():
    data = request.get_json()
    query = data.get('query') if data else None
    if not query:
        return jsonify({'error': 'No text provided'}), 400
    
    try:
        result = handle_new_query(query)
        return jsonify(result)
    except Exception as e:
        # Log the error and provide a user-friendly message
        print(f"An error occurred: {str(e)}")
        return jsonify({'error': 'Failed to handle query'}), 500

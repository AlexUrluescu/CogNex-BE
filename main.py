
from aiModelClass import AskChat
import os
from PyPDF2 import PdfReader
# from aiAzureModel import AskAzure

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
app = Flask(__name__)

CORS(app, origins=['http://localhost:3000'])

pdf_directory = '/Users/alexandreurluescu/Documents/personal work/CogNex/CogNex-BE/server/uploads'

@app.route('/api/pdfs', methods=['GET'])
def get_pdfs():
    # List all PDF files in the directory
    pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
    return jsonify(pdf_files)


@app.route('/pdfs/<path:filename>', methods=['GET'])
def serve_pdf(filename):
    # Ensure that the requested file is a PDF
    if not filename.lower().endswith('.pdf'):
        return "Not a PDF file", 400
    
    # Get the full path of the requested PDF file
    file_path = os.path.join(pdf_directory, filename)
    
    # Check if the file exists
    if not os.path.isfile(file_path):
        return "PDF not found", 404
    
    # Serve the PDF file
    return send_from_directory(pdf_directory, filename)

@app.route('/test', methods=['GET'])
def handleTest():
    name = 'Alex'

    nameTest = {"name": name}

    return jsonify(nameTest)


@app.route('/test2', methods=['POST'])
def handleTest2():
    query = request.json
    print(query)

    chatMessage = {"role": "chat", "message": 'works'}

    return jsonify(chatMessage)


@app.route('/register', methods=['POST'])
def handleUserRegister():
    query = request.json

    user = query['user']
    
    print(user)

    chatMessage = {'ok': True, 'message': "user received"}

    return jsonify(chatMessage), 200

    

# @app.route('/chat', methods=['POST']) 
# def handle_to_server():

#     query = request.json
#     print(query)

#     # answer = chat.answering(query["message"])

#     chatMessage = {"role": "chat", "message": answer}

#     print(chatMessage)

#     return jsonify(chatMessage)


@app.route('/extract', methods=['POST']) 
def extract_content():

    # Set the folder to store uploaded PDFs
    UPLOAD_FOLDER = 'uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Ensure the upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF part'})

    pdf = request.files['pdf']
    if pdf.filename == '':
        return jsonify({'error': 'No selected file'})
    
    # Save the PDF file
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf.filename)
    pdf.save(pdf_path)

    # Read the content of the PDF
    pdf_content = read_pdf_content(pdf_path)
    print(pdf_content)

    return jsonify({'message': 'PDF uploaded successfully'})

def read_pdf_content(pdf_path):
    pdf_content = ''
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            pdf_content += pdf_reader.pages[page_num].extract_text()
    return pdf_content


if __name__ == '__main__':
    app.run( port=5000, debug = True )
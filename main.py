
from aiModelClass import AskChat
import os
from PyPDF2 import PdfReader
# from aiAzureModel import AskAzure

from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)

CORS(app, origins=['http://localhost:3000'])

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

from aiModelClass import AskChat
import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv
# from aiAzureModel import AskAzure

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_pymongo import pymongo
app = Flask(__name__)

load_dotenv()

ROUTE = os.environ.get("ROUTE")

CORS(app, origins=[ROUTE])

CONNECTION_STRING_MONGODB = os.environ.get("CONNECTION_STRING_MONGODB")

client = pymongo.MongoClient(CONNECTION_STRING_MONGODB, tls=True, tlsAllowInvalidCertificates=True)
db = client.get_database('AiChat')

app.config['USERS_DOCUMENTS'] = '/Users/alexandreurluescu/Documents/personal work/CogNex/CogNex-BE/server/users_documents'
 
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


@app.route('/login', methods=['POST'])
def handleUserLogin():
    query = request.json
    user = query['user']
    userFound = db.users.find_one({"email": user['email']})

    if(userFound == None):
        return jsonify({'message': "no user found", 'ok': False, "user": None})

    if(userFound['password'] != user['password']):
        return jsonify({"message": "password incorrect", 'ok': False, "user": None})
    
    userFound['_id'] = str(userFound['_id'])

    return jsonify({"message": 'success', 'ok': True, 'user': userFound})


@app.route('/register', methods=['POST'])
def handleUserRegister():
    query = request.json
    user = query['user']

    result = db.users.insert_one(user)

    userStored = db.users.find_one({"_id": result.inserted_id})
    userStored['_id'] = str(userStored['_id'])

    user_folder_path = os.path.join(app.config['USERS_DOCUMENTS'], userStored['_id'])
    os.makedirs(user_folder_path)

    return jsonify({"message": "success", "ok": True, "user": userStored}), 200

    

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
    if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF part'})

    pdf = request.files['pdf']
    userId = request.form['userId']

    if pdf.filename == '':
        return jsonify({'error': 'No selected file'})
    
    # Save the PDF file
    subdirectory_path = os.path.join(app.config['USERS_DOCUMENTS'], userId)
    pdf_path = os.path.join(subdirectory_path, pdf.filename)
    pdf.save(pdf_path)

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
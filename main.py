
import glob
from aiModelClass import AskChat
import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from bson.objectid import ObjectId
# from aiAzureModel import AskAzure
from utils import Utils

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_pymongo import pymongo
from utils import Utils
app = Flask(__name__)

load_dotenv()

ROUTE = os.environ.get("ROUTE")

CORS(app)

CONNECTION_STRING_MONGODB = os.environ.get("CONNECTION_STRING_MONGODB")


utils = Utils()

chromaDbPath = 'testing'

client = pymongo.MongoClient(CONNECTION_STRING_MONGODB, tls=True, tlsAllowInvalidCertificates=True)
db = client.get_database('AiChat')

app.config['USERS_DOCUMENTS'] = '/Users/alexandreurluescu/Documents/current work/CogNex/CogNex-BE/server/users_documents'
app.config['USERS_DOCUMENTS2'] = '/Users/alexandreurluescu/Documents/current work/CogNex/CogNex-BE/server/users_documents2'
 
pdf_directory = '/Users/alexandreurluescu/Documents/current work/CogNex/CogNex-BE/server/uploads'

user_documents_global_directory = '/Users/alexandreurluescu/Documents/current work/CogNex/CogNex-BE/server/users_documents'



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
    
    file = send_from_directory(pdf_directory, filename)
    
    # Serve the PDF file
    return file

def testing(subDirectory, filename):
    # Ensure that the requested file is a PDF
    if not filename.lower().endswith('.pdf'):
        return "Not a PDF file", 400
    
    # Get the full path of the requested PDF file
    file_path = os.path.join(subDirectory, filename)
    
    # Check if the file exists
    if not os.path.isfile(file_path):
        return "PDF not found", 404
    
    file = send_from_directory(subDirectory, filename)

    print(file)
    
    # Serve the PDF file
    return file


@app.route('/user-pdfs/<path:userId>', methods=['GET'])
def serve_pdf123(userId):


    pdf_files = []

    test = []

    for root, dirs, files in os.walk(user_documents_global_directory):
        if userId in dirs:
            userId_dir = os.path.join(root, userId)
            pdf_files.extend([os.path.basename(file) for file in os.listdir(userId_dir) if file.endswith('.pdf')])

    subDirectoryPath = os.path.join(user_documents_global_directory, userId)
    

    # for pdf in pdf_files:
    #     print(pdf)
    #     fileName = testing(subDirectoryPath, pdf)
    #     test.append(fileName)

    pdf = pdf_files[0]
    fileName = testing(subDirectoryPath, pdf)
    test.append(fileName)

    for chat in test:
        chat = str(chat)

    return test

    # Get the full path of the requested PDF file
    # file_path = os.path.join(user_documents_global_directory, userId)
    
    # # Check if the file exists
    # if not os.path.isfile(file_path):
    #     return "PDF not found", 404
    
    # file = send_from_directory(user_documents_global_directory, filename)
    
    # # Serve the PDF file
    # return file


# def list_pdf_files(directory):
#     pdf_files = []
#     for root, dirs, files in os.walk(directory):
#         if "sub2" in dirs:
#             sub2_dir = os.path.join(root, "sub2")
#             pdf_files.extend([os.path.join(sub2_dir, file) for file in os.listdir(sub2_dir) if file.endswith('.pdf')])
#     return pdf_files

# directory = "/path/to/your/directory"
# pdf_files = list_pdf_files(directory)
# print("PDF files in the 'sub2' directories:")
# for pdf_file in pdf_files:
#     print(pdf_file)

@app.route("/users", methods=['GET'])
def get_all_users():
    users = list(db.users.find({}))

    for user in users:
        user['_id'] = str(user['_id'])

    return jsonify({"message": 'success', 'ok': True, 'users': users})





@app.route("/chats", methods=['GET'])
def get_all_chats():
    chats = list(db.chats.find({}))

    for chat in chats:
        chat['_id'] = str(chat['_id'])

    return jsonify({"message": 'success', 'ok': True, 'chats': chats})


@app.route('/testApi/<path:userId>', methods=['GET'])
def serve_pdf2(userId):

    user_documents_path = os.path.join(app.config['USERS_DOCUMENTS'], userId)

    # Get the full path of the requested PDF file
    files = os.listdir(user_documents_path)

    # Serve the PDF file
    # return send_from_directory(pdf_directory, filename)
    return jsonify({"ok": True, "filesName": files})

@app.route('/currentUser/<path:userId>', methods=['GET'])
def handleTest(userId):
    print(userId)

    userFound = db.users.find_one({'_id': ObjectId(userId)})

    userFound['_id'] = str(userFound['_id'])

    return jsonify({"message": 'success', 'ok': True, 'user': userFound})


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


@app.route('/info-chat', methods=['POST']) 
def getDocsFromChromaCollectByChat():
    query = request.json
    chatId = query['chatId']
    question = query['query']

    results = utils.getRevevantInfoFromDb(chromaDbPath, chatId, question)

    return jsonify({"message": 'success', 'ok': True, 'documents': results})



@app.route('/subscribed', methods=['POST'])
def handleUserSubscribed():
    query = request.json
    userId = query['userId']
    chatId = query['chatId']

    chatUpdated = db.chats.find_one_and_update(
        {'_id': ObjectId(chatId)},
        {'$addToSet': {'users': userId}}, 
        return_document=True
    )

    if chatUpdated:
        chatUpdated['_id'] = str(chatUpdated['_id'])
        print(chatUpdated['users'])
        return jsonify({"message": 'success', 'ok': True, 'chat': chatUpdated})
    else:
        return jsonify({"message": 'Chat not found', 'ok': False}), 404


@app.route('/register', methods=['POST'])
def handleUserRegister():
    query = request.json
    user = query['resgiterUser']

    result = db.users.insert_one(user)

    userStored = db.users.find_one({"_id": result.inserted_id})
    userStored['_id'] = str(userStored['_id'])

    user_folder_path = os.path.join(app.config['USERS_DOCUMENTS'], userStored['_id'])
    os.makedirs(user_folder_path)

    user_folder_path2 = os.path.join(app.config['USERS_DOCUMENTS2'], userStored['_id'])
    os.makedirs(user_folder_path2)

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
    print(f"req {request.files}")
    if 'pdfs' not in request.files:
        return jsonify({'error': 'No PDF part'})

    pdfs = request.files.getlist('pdfs')
    userId = request.form['userId']

    print(f"pdf {pdfs}")
    print(f"userId {userId}")

    for pdf in pdfs:

        if pdf.filename == '':
            return jsonify({'error': 'No selected file'})
        
        # Save the PDF file
        subdirectory_path = os.path.join(app.config['USERS_DOCUMENTS2'], userId)
        pdf_path = os.path.join(subdirectory_path, pdf.filename)
        pdf.save(pdf_path)

        user = db.users.find_one({'_id': ObjectId(userId)})

        print(user)

        if user:
            # Modify the projects field
            updated_files = user.get('files', [])
            updated_files.append(pdf.filename)

            # Update the user document
            db.users.update_one(
                {'_id': ObjectId(userId)},
                {'$set': {'files': updated_files}}
            )

            
        else:
            return 'User not found', 404
    
    # utils.storeDataIntoChroma(subdirectory_path, chromaDbPath, userId)
        
    return jsonify({'message': 'PDF uploaded successfully', "ok": True})


def delete_files_in_directory(directory):
    # Get a list of all files within the directory
    files = glob.glob(os.path.join(directory, "*"))
    
    # Iterate over the list of files
    for file in files:
        try:
            # Delete each file
            os.remove(file)
            print(f"Deleted: {file}")
        except Exception as e:
            print(f"Error deleting {file}: {e}")



@app.route('/create_chat', methods=['POST']) 
def create_chat_room():
    query = request.json
    chat = query['chat']

    print("chat", chat)
    print("chatFiles", chat['files'])

    creatorId = chat['creator']

    savedChat = db.chats.insert_one(chat)

    chatStored = db.chats.find_one({"_id": savedChat.inserted_id})
    chatStored['_id'] = str(chatStored['_id'])

    subdirectory_path = os.path.join(app.config['USERS_DOCUMENTS2'], str(chatStored['creator']))
    subdirectory_path2 = os.path.join(app.config['USERS_DOCUMENTS'], str(chatStored['creator']))

    utils.storeDataIntoChroma(subdirectory_path, chromaDbPath, str(chatStored['_id']))

    utils.move_files(subdirectory_path, subdirectory_path2)

    return jsonify({"message": "success", "ok": True, "chat": chatStored}), 200



def read_pdf_content(pdf_path):
    pdf_content = ''
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            pdf_content += pdf_reader.pages[page_num].extract_text()
    return pdf_content


if __name__ == '__main__':
    app.run( port=5000, debug = True )
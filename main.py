
import base64
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
from bson import Binary
app = Flask(__name__)

load_dotenv()

ROUTE = os.environ.get("ROUTE")

CORS(app)

CONNECTION_STRING_MONGODB = os.environ.get("CONNECTION_STRING_MONGODB")


utils = Utils()

chromaDbPath = 'testing'
chromaDbTeleportsPath = 'teleports'

client = pymongo.MongoClient(CONNECTION_STRING_MONGODB, tls=True, tlsAllowInvalidCertificates=True)
db = client.get_database('AiChat')

app.config['USERS_DOCUMENTS'] = '/Users/alexandreurluescu/Documents/current work/CogNex/CogNex-BE/server/users_documents'
app.config['USERS_DOCUMENTS2'] = '/Users/alexandreurluescu/Documents/current work/CogNex/CogNex-BE/server/users_documents2'
 
pdf_directory = '/Users/alexandreurluescu/Documents/current work/CogNex/CogNex-BE/server/uploads'

user_documents_global_directory = '/Users/alexandreurluescu/Documents/current work/CogNex/CogNex-BE/server/users_documents'

PDFS = []
FILES = []

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


@app.route('/pdfs', methods=['POST'])
def serve_pdf3():
    query = request.json
    filename = query['filename']
    userId = query['userId']
    # Ensure that the requested file is a PDF
    if not filename.lower().endswith('.pdf'):
        return "Not a PDF file", 400
    
    reletivPathUsersDocs = 'users_documents'
    userDirectoryDocsPath = os.path.join(reletivPathUsersDocs, userId)
    
    # Get the full path of the requested PDF file
    file_path = os.path.join(userDirectoryDocsPath, filename)
    
    # Check if the file exists
    if not os.path.isfile(file_path):
        return "PDF not found", 404
    
    file = send_from_directory(userDirectoryDocsPath, filename)
    
    # Serve the PDF file
    return file

@app.route('/add-docs', methods=['POST']) 
def add_cods():
    query = request.json
    chat = query['chat']


    print("chat", chat)
    print("chatFiles", chat['files'])

    # creatorId = chat['creator']

    # savedChat = db.chats.insert_one(chat)

    # chatStored = db.chats.find_one({"_id":  ObjectId(chat['_id'])})
    # chatStored['_id'] = str(chatStored['_id'])

    subdirectory_path = os.path.join(app.config['USERS_DOCUMENTS2'], str(chat['creator']))
    
    files = get_file_names(subdirectory_path)

    print(f"FILES2: {files}")
    print("   ------------------------- ")
    print("   ------------------------- ")
    print("   ------------------------- ")
    print("   ------------------------- ")
    print("   ------------------------- ")

    result = []


    difference_list = utils.storeDataIntoChromaAddDocs(subdirectory_path, chromaDbPath, str(chat['_id']), files[0])

    fileObject = {'name': files[0],
                    'documentId': difference_list
    }

    result.append(fileObject)

    print(f'RESULT: {result}')
    
    result.extend(chat['files'])
    merged_array = result

    print(f"MERGED: {merged_array}")

    chatUpdated = db.chats.find_one_and_update(
            {'_id': ObjectId(chat['_id'])},
            {'$set': {'files': merged_array}}, 
        return_document=True
    )

    if chatUpdated:
        chatUpdated['_id'] = str(chatUpdated['_id'])
        return jsonify({"message": 'success', 'ok': True, 'chat': chatUpdated})
    else:
        return jsonify({"message": 'Chat not found', 'ok': False}), 500


@app.route('/delete-docs', methods=['DELETE'])
def delete_files_from_chat():
    query = request.json
    documentId = query['documentId']
    chatId = query['chatId']

    chatFound = db.chats.find_one({'_id': ObjectId(chatId)})

    # chatFound['files'].remove(filename)
    print(documentId)
    print(chatFound['files'])

    array_of_objects = [obj for obj in chatFound['files'] if obj['documentId'] != documentId]

    db.chats.update_one(
                {'_id': ObjectId(chatId)},
                {'$set': {'files': array_of_objects}}
            )

    chatFound2 = db.chats.find_one({'_id': ObjectId(chatId)})

    chatFound2['_id'] = str(chatFound2['_id'])

    success = utils.deleteSpecificDataFromChromaDb(chromaDbPath, chatId, documentId)

    if(success):
        return jsonify({"message": 'success', 'ok': True, 'chat': chatFound2})
    
    else:
        return jsonify({"message": 'failed', 'ok': False})




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


@app.route("/teleports", methods=['GET'])
def get_all_teleports():
    teleports = list(db.teleports.find({}))

    for teleport in teleports:
        teleport['_id'] = str(teleport['_id'])

    return jsonify({"message": 'success', 'ok': True, 'teleports': teleports})


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

    # if(userFound['password'] != user['password']):
    #     return jsonify({"message": "password incorrect", 'ok': False, "user": None})
    
    userFound['_id'] = str(userFound['_id'])
    # image_data_base64 = base64.b64encode(userFound['photo'].read()).decode("utf-8")
    # userFound['photo'] = image_data_base64

    return jsonify({"message": 'success', 'ok': True, 'user': userFound})


@app.route('/info-chat', methods=['POST']) 
def getDocsFromChromaCollectByChat():
    query = request.json
    chatId = query['chatId']
    question = query['query']

    print(chatId)

    results = utils.getRevevantInfoFromDb(chromaDbPath, chatId, question)

    llmResponse = utils.getLlmResponse(query=question, docs_prepared=results)

    return jsonify({"message": 'success', 'ok': True, 'response': llmResponse})



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
    

@app.route('/unsubscribed', methods=['POST'])
def handleUserUnsubscribed():
    query = request.json
    userId = query['userId']
    chatId = query['chatId']

    chatFound = db.chats.find_one({"_id": ObjectId(chatId)})

    array_of_objects = [obj for obj in chatFound['users'] if obj != userId]

    db.chats.update_one(
                {'_id': ObjectId(chatId)},
                {'$set': {'users': array_of_objects}}
            )

    chatFound2 = db.chats.find_one({'_id': ObjectId(chatId)})


    if chatFound2:
        chatFound2['_id'] = str(chatFound2['_id'])
        print(chatFound2['users'])
        return jsonify({"message": 'success', 'ok': True, 'chat': chatFound2})
    else:
        return jsonify({"message": 'Chat not found', 'ok': False}), 404


@app.route('/add-review', methods=['POST'])
def handleAddReview():
    query = request.json
    review = query['review']
    chatId = query['chatId']

    chatUpdated = db.chats.find_one_and_update(
        {'_id': ObjectId(chatId)},
        {'$addToSet': {'reviews': review}}, 
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

@app.route('/upload-photo', methods=['POST']) 
def upload_photo():
    if 'images' not in request.files:
        return jsonify({'error': 'No PDF part'})

    images = request.files.getlist('images')

    print(images)
    print(images[0])

    image_data = images[0].read()

    image_doc = {'image': Binary(image_data)}

    test2 = {
        'name': 'Alex'
    }

    print("intraaa1")

    user = db.poze.insert_one(image_doc)
    db.users.update_one({'_id': ObjectId('65e46bd58d312e7ab5895adf')}, {'$set': {'photo': image_doc['image']}})
    print(user)

    chatStored = db.poze.find_one({"name": 'Alex'})

    print("intraaaa")
    return jsonify({'message': 'Images uploaded successfully', "ok": True})


@app.route('/extract', methods=['POST']) 
def extract_content():
    # print(f"req {request.files}")
    if 'pdfs' not in request.files:
        return jsonify({'error': 'No PDF part'})

    pdfs = request.files.getlist('pdfs')
    userId = request.form['userId']

    print(f"PDFS {pdfs}")
    # print(f"userId {userId}")

    for pdf in pdfs:

        if pdf.filename == '':
            return jsonify({'error': 'No selected file'})
        
        # Save the PDF file
        subdirectory_path = os.path.join(app.config['USERS_DOCUMENTS2'], userId)
        pdf_path = os.path.join(subdirectory_path, pdf.filename)
        print(f"PDF PATH: {pdf_path}")
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
    
    files = get_file_names(subdirectory_path)

    print(f"FILES: {files}")
    print(f"len(pdfs) {len(pdfs)}")
    print(f"len(files) {len(files)}")

    if(len(files) == len(pdfs)):
    # utils.storeDataIntoChroma(subdirectory_path, chromaDbPath, userId)
        return jsonify({'message': 'PDF uploaded successfully', "ok": True})
    else:
        return jsonify({'message': 'error', "ok": False})



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

def count_files(directory_path):
    files = os.listdir(directory_path)
    file_count = len([file for file in files if os.path.isfile(os.path.join(directory_path, file))])
    return file_count

def get_file_names(directory_path):
    files = os.listdir(directory_path)
    file_names = [file for file in files if os.path.isfile(os.path.join(directory_path, file))]
    return file_names

@app.route('/create_chat', methods=['POST']) 
def create_chat_room():
    query = request.json
    chat = query['chat']

    # files2 = get_file_names('users_documents2/662b5125b794abdb37153b58')

    # print(f"FILES2: {files2}")
    print("chat", chat)
    print("chatFiles", chat['files'])

    creatorId = chat['creator']

    savedChat = db.chats.insert_one(chat)

    chatStored = db.chats.find_one({"_id": savedChat.inserted_id})
    chatStored['_id'] = str(chatStored['_id'])

    subdirectory_path = os.path.join(app.config['USERS_DOCUMENTS2'], str(chatStored['creator']))
    
    files = get_file_names(subdirectory_path)

    print(f"FILES2: {files}")
    print("   ------------------------- ")
    print("   ------------------------- ")
    print("   ------------------------- ")
    print("   ------------------------- ")
    print("   ------------------------- ")

    result = []

    for file in files:
        documentIds = utils.storeDataIntoChroma(subdirectory_path, chromaDbPath, str(chatStored['_id']), file)

        print(f'random_uuid_str2: {documentIds}')

        fileObject = {'name': file,
                    'documentId': documentIds
                    }

        result.append(fileObject)

    
    print(f"RESULT: {result}")

    

    chatUpdated = db.chats.find_one_and_update(
        {'_id': ObjectId(chatStored['_id'])},
        {'$set': {'files': result}}, 
        return_document=True
    )

    chatUpdated['_id'] = str(chatUpdated['_id'])


    if(chatUpdated['_id'] != ''):
        return jsonify({"message": "success", "ok": True, "chat": chatUpdated}), 200
    
    else:
         return jsonify({"message": "error", "ok": False, "chat": None}), 500
    

@app.route('/removing_old_pdfs', methods=['POST']) 
def remove_old_pdfs():
    query = request.json
    creator = query['creator']

    print(f"creator {creator}")

    subdirectory_path = os.path.join(app.config['USERS_DOCUMENTS2'], creator)
    subdirectory_path2 = os.path.join(app.config['USERS_DOCUMENTS'], creator)

    utils.move_files(subdirectory_path, subdirectory_path2)

    return jsonify({"message": "success", "ok": True, "success": True }), 200



@app.route('/create_teleport', methods=['POST']) 
def create_teleport():
    query = request.json
    teleport = query['teleport']
    print(teleport)
    savedTeleport = db.teleports.insert_one(teleport)

    teleportStored = db.teleports.find_one({"_id": savedTeleport.inserted_id})
    teleportStored['_id'] = str(teleportStored['_id'])

    # utils.storeDataIntoChromaTeleport()


    print(teleportStored)

    return jsonify({"message": "success", "ok": True, "teleport": teleportStored}), 200

def read_pdf_content(pdf_path):
    pdf_content = ''
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            pdf_content += pdf_reader.pages[page_num].extract_text()
    return pdf_content


if __name__ == '__main__':
    app.run( port=5000, debug = True )
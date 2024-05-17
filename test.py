from utils import Utils
import chromadb
import os

chromaDbPath = 'testing'
collectionName = '6634d26f1e32d0ffb14979eb'

chromadbTeleport = 'your_database_path'

chats = ['663494c4caaba6ae1cdf725f', '6630f3545922b25e2b45e1cb']

path = 'users_documents2/662b4b111d27688666af06ed'

source = '/Users/alexandreurluescu/Documents/current work/CogNex/CogNex-BE/server/users_documents2/662b5125b794abdb37153b58/PersonalData1.pdf'

src = '3d3b6bc1-9013-4d8d-a28a-f29e1f8e28a7'

utils = Utils()

teleportId = '664361c9a276efad4206bf70'
chatCollection = '6641c74701c21984c126ce9d'

data = utils.getDataFromChromaDb(chromaDbPath = chromadbTeleport, collectionName=teleportId)
print(data)
print(data['ids'])

# utils.deleteChatFromTeleportChromaDb(chromaDbPathChats='testing', collectionName='6634b4693ea576abb4d6329b', chromaDbTeleports= chromadbTeleport, collectionTeleport=teleportId)

# 168210ad-3cc4-497d-8636-d4d6552031d5', '24ba6cda-6d10-4d3d-abd5-52f1ed61fb20
# utils.deleteSpecificDataFromChromaDb(chromaDbPath, collectionName, src)

# utils.create_teleport(collectionName=collectionName, chats=chats)

# def get_file_names(directory_path):
#     files = os.listdir(directory_path)
#     file_names = [file for file in files if os.path.isfile(os.path.join(directory_path, file))]
#     return file_names


# subdirectory_path = 'users_documents2/662b5125b794abdb37153b58'

# files = get_file_names(subdirectory_path)

# print(files)
# print(len(files))

# files = get_file_names(subdirectory_path)
# result = []
# for file in files:
#     documentId = utils.storeDataIntoChroma(subdirectory_path, chromaDbPath, 'test2006', file)

#     fileObject = {'name': file,
#                   'documentId': documentId}

#     result.append(fileObject)

#     print(f"documentId: {documentId}")


# print(result)

# success = utils.storeDataIntoChroma(docsPath=path, chromaDbPath=chromaDbPath, collectionName='662e49b1c8e348a962e2580d')

# print(success)

# utils.storeDataIntoChroma(docsPath=path, chromaDbPath=chromaDbPath, collectionName='test2')


# Create a ChromaDB client (you can use either PersistentClient or HttpClient)
# client = chromadb.PersistentClient(path="your_database_path")

# # Create a new collection (replace "my_collection" with your desired collection name)
# newCollection = client.create_collection("my_collection")
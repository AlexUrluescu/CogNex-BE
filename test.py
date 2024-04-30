from utils import Utils
import chromadb
import os

chromaDbPath = 'testing'
collectionName = '6630d26010acddc58c89afab'

path = 'users_documents2/662b4b111d27688666af06ed'

source = '/Users/alexandreurluescu/Documents/current work/CogNex/CogNex-BE/server/users_documents2/662b5125b794abdb37153b58/PersonalData1.pdf'

src = '3d3b6bc1-9013-4d8d-a28a-f29e1f8e28a7'

utils = Utils()

data = utils.getDataFromChromaDb(chromaDbPath, collectionName='6630da2d02a3f7e7619a9ba5')
print(data)

# utils.deleteSpecificDataFromChromaDb(chromaDbPath, collectionName, src)


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
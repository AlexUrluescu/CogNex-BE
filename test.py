from utils import Utils
import chromadb

chromaDbPath = 'testing'
collectionName = '661968510642d8c2769ca19a'


utils = Utils()

data = utils.getDataFromChromaDb(chromaDbPath, collectionName)

print(data)


# Create a ChromaDB client (you can use either PersistentClient or HttpClient)
client = chromadb.PersistentClient(path="your_database_path")

# Create a new collection (replace "my_collection" with your desired collection name)
newCollection = client.create_collection("my_collection")
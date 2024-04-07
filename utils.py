from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.document_loaders import TextLoader, DirectoryLoader, PyPDFLoader
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
import chromadb
import shutil
import os

class Utils():
 
        
    def storeDataIntoChroma(self, docsPath: str, chromaDbPath: str, collectionName: str):
        loader = DirectoryLoader(docsPath, glob="./*.pdf", loader_cls=PyPDFLoader)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=300)
        docs = text_splitter.split_documents(documents)

        embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

        database = Chroma.from_documents(docs, embedding_function, persist_directory=chromaDbPath, collection_name=collectionName)

        data = database._collection.get()

        print(data['documents'])

        return data['documents']
    

    def storeSpecificPdfDataIntoChroma(self, pdfPath: str, chromaDbPath: str, collectionName: str):
        loader = PyPDFLoader(pdfPath)
        document = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=300)
        docs = text_splitter.split_documents(document)

        embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

        database = Chroma.from_documents(docs, embedding_function, persist_directory=chromaDbPath, collection_name=collectionName)

        data = database._collection.get()

        print(data['documents'])

        return data['documents']
    

    def getDataFromChromaDb(self, chromaDbPath: str, collectionName: str):
        client = chromadb.PersistentClient(path=chromaDbPath)
        collection = client.get_collection(collectionName)

        data = collection.get()

        print(data['documents'])

        return data
    

    def getRevevantInfoFromDb(self, chromaDbPath: str, collectionName: str, query: str):
        client = chromadb.PersistentClient(path=chromaDbPath)
        collection = client.get_collection(collectionName)

        results = collection.query(
            query_texts=[query],
            n_results=1
        )

        print(results)

        return results

        # retriever = collection.as_retriever(search_type="similarity", search_kwargs = {"k": 5})

        # docs = retriever.get_relevant_documents(query)

        # print(docs)


    def move_files(self, source_dir, destination_dir):
        # Ensure the destination directory exists, create it if it doesn't
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        # Get a list of all files in the source directory
        files = os.listdir(source_dir)

        # Move each file to the destination directory
        for file in files:
            source_file = os.path.join(source_dir, file)
            destination_file = os.path.join(destination_dir, file)
            try:
                shutil.move(source_file, destination_file)
                print(f"Moved: {source_file} to {destination_file}")
            except Exception as e:
                print(f"Error moving {source_file} to {destination_file}: {e}")
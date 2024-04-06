from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.document_loaders import TextLoader, DirectoryLoader, PyPDFLoader
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings

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
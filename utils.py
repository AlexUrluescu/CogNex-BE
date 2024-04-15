from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.document_loaders import TextLoader, DirectoryLoader, PyPDFLoader
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
import chromadb
import shutil
import os
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
# from langchain_openai import OpenAI
from langchain.chat_models import ChatOpenAI
class Utils():

    def __init__(self) -> ChatOpenAI:

        self.openai_api_key = "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"
        

        self.template = """QUESTION: {query}

            INFORMATION: {docs_prepared}

            Please provide a reponse on base the INFORMATION.

            If you dont find anything similar in the INFORMATION, please responde with: "I dont have this information" """


    def getLlmResponse(self, query, docs_prepared):

        print(query)

        prompt = PromptTemplate.from_template(self.template)
        llm = ChatOpenAI(
            model_name='gpt-3.5-turbo-16k',
            temperature=0.9,
            openai_api_key=self.openai_api_key,
            max_tokens=50
        )
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        response = llm_chain.invoke({"query": query, "docs_prepared": docs_prepared})

        print(response)

        return response
 
        
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

        print(collectionName)

        return results['documents'][0][0]

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
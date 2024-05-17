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
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
import uuid
class Utils():

    def __init__(self) -> ChatOpenAI:

        self.openai_api_key = "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"
        
        self.chromaDbTeleportsPath = 'testing'

        # self.template = """QUESTION: {query}

        #     INFORMATION: {docs_prepared}

        #     Please provide a reponse on base the INFORMATION.

        #     If you dont find anything similar in the INFORMATION, please responde with: "I dont have this information" """


    def process_llm_response(self, llm_response):
        print(llm_response['result'])
        print("\n\nSources:")
        for source in llm_response["source_documents"]:
            print(source.metadata['source'])
        
        return llm_response['result']
    
    def getLlmResponseForChat(self, question, retriever, context):

        print(question)
        
        question = question
        context = context
        # question = 'Care este email-ul domnului Urluescu Alexandre, care are domeniul @ulbsibiu.ro?'
        template = """Use all pieces of context to answer the question at the end and try not mix up the informations of them. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use three sentences maximum. Keep the answer as concise as possible. Always answer in Romanian language. 
        {context}s
        Question: {question}
        If you dont know the answer, responde with a kind answer
        """

        QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

        # prompt = PromptTemplate.from_template(self.template)
        llm = ChatOpenAI(
            # model_name='gpt-3.5-turbo-16k',
            model_name='gpt-4',
            temperature=0.9,
            openai_api_key=self.openai_api_key,
            max_tokens=200
        )
        chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever = retriever, return_source_documents = True, chain_type_kwargs={"prompt": QA_CHAIN_PROMPT} )
        llm_response = chain(question)
        response = self.process_llm_response(llm_response)
        # llm_chain = LLMChain(prompt=prompt, llm=llm)
        # response = llm_chain.invoke({"query": query, "docs_prepared": docs_prepared})

        print(response)

        return response
 

    def getLlmResponse(self, question, retriever, context):

        print(question)
        
        question = question
        context = context
        # question = 'Care este email-ul domnului Urluescu Alexandre, care are domeniul @ulbsibiu.ro?'
        template = """Use all pieces of context to answer the question at the end and try not mix up the informations of them. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use three sentences maximum. Keep the answer as concise as possible. Always answer in Romanian language. 
        {context}s
        Question: {question}
        If you dont know the answer, responde with a kind answer
        """

        QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

        # prompt = PromptTemplate.from_template(self.template)
        llm = ChatOpenAI(
            # model_name='gpt-3.5-turbo-16k',
            model_name='gpt-4',
            temperature=0.9,
            openai_api_key=self.openai_api_key,
            max_tokens=700
        )
        chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever = retriever, return_source_documents = True, chain_type_kwargs={"prompt": QA_CHAIN_PROMPT} )
        llm_response = chain(question)
        response = self.process_llm_response(llm_response)
        # llm_chain = LLMChain(prompt=prompt, llm=llm)
        # response = llm_chain.invoke({"query": query, "docs_prepared": docs_prepared})

        print(response)

        return response
 
        
    def storeDataIntoChroma(self, docsPath: str, chromaDbPath: str, collectionName: str, file: str):
        success = True
        random_uuid = uuid.uuid4()

        try:
            loader = DirectoryLoader(docsPath, glob=file, loader_cls=PyPDFLoader)
            documents = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=300)
            docs = text_splitter.split_documents(documents)

            print(f'DOCS 2: {docs}')
            print(' ----------------------------------------------------- ')
            print(' ----------------------------------------------------- ')
            print(' ----------------------------------------------------- ')
            print(' ----------------------------------------------------- ')
            print(' ----------------------------------------------------- ')

            embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

            # client = chromadb.PersistentClient(path=chromaDbPath)
            # collection = client.get_collection(collectionName)
            # data = collection.get()

            # currentIds = data['ids']
            # print(f'CURRENT IDS: {currentIds}')
            # print(' ----------------------------------------------------- ')
            # print(' ----------------------------------------------------- ')
                
            database = Chroma.from_documents(docs, embedding_function, persist_directory=chromaDbPath, collection_name=collectionName)

            data = database._collection.get()
            newIds = data['ids']

            # setCurrentIds = set(currentIds)
            # setNewIds = set(newIds)

            # difference = setNewIds - setCurrentIds

            # difference_list = list(difference)

            # print(f"DATA {data}")

            return newIds
        except:
            success = False
            return success
        

    def storeDataIntoChromaAddDocs(self, docsPath: str, chromaDbPath: str, collectionName: str, file: str):
        success = True

        try:
            loader = DirectoryLoader(docsPath, glob=file, loader_cls=PyPDFLoader)
            documents = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=300)
            docs = text_splitter.split_documents(documents)

            print(f'DOCS 2: {docs}')
            print(' ----------------------------------------------------- ')
            print(' ----------------------------------------------------- ')
            print(' ----------------------------------------------------- ')
            print(' ----------------------------------------------------- ')
            print(' ----------------------------------------------------- ')

            embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

            client = chromadb.PersistentClient(path=chromaDbPath)
            collection = client.get_collection(collectionName)
            data = collection.get()

            currentIds = data['ids']
            print(f'CURRENT IDS: {currentIds}')
            print(' ----------------------------------------------------- ')
            print(' ----------------------------------------------------- ')
                
            database = Chroma.from_documents(docs, embedding_function, persist_directory=chromaDbPath, collection_name=collectionName)

            data = database._collection.get()
            newIds = data['ids']

            setCurrentIds = set(currentIds)
            setNewIds = set(newIds)

            difference = setNewIds - setCurrentIds

            difference_list = list(difference)

            print(f"DATA {data}")

            return difference_list
        except:
            success = False
            return success
    

    def storeDataIntoChromaTeleport(self, chromaDbPath: str, collectionName):
        # loader = DirectoryLoader(docsPath, glob="./*.pdf", loader_cls=PyPDFLoader)
        # documents = loader.load()

        data = self.getDataFromChromaDb(chromaDbPath, collectionName)

        # text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=300)
        # docs = text_splitter.split_documents(documents)

        # embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

        # database = Chroma.from_documents(docs, embedding_function, persist_directory=chromaDbPath, collection_name=collectionName)

        # data = database._collection.get()

        print(data['documents'])

        # return data['documents']
    

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

        # print(data['documents'])

        return data
    

    def deleteDataFromChromaDb(self, chromaDbPath: str, collectionName: str):
        client = chromadb.PersistentClient(path=chromaDbPath)
        collection = client.get_collection(collectionName)

        data = collection.delete(
            ids=['2ef19a59-7f4c-43dd-a62e-82f692b57ea6'],
            where={'source': '/Users/alexandreurluescu/Documents/current work/CogNex/CogNex-BE/server/users_documents2/662b5125b794abdb37153b58/Personal Data (2).pdf'}
        )

        print(data)

    def deleteSpecificDataFromChromaDb(self, chromaDbPath: str, collectionName: str, source: str):
        print(collectionName)
        try:
            client = chromadb.PersistentClient(path=chromaDbPath)
            collection = client.get_collection(collectionName)

            # collection.delete(ids="2ef19a59-7f4c-43dd-a62e-82f692b57ea6")
            collection.delete(ids=source)

            return True
        except:
            print('error')
    

    def deleteChatFromTeleportChromaDb(self, chromaDbPathChats: str, collectionName: str, chromaDbTeleports: str, collectionTeleport: str):
        print(collectionName)
        
        try:

            data = self.getDataFromChromaDb(chromaDbPathChats, collectionName=collectionName)
            print(data['ids'])
            ids = data['ids']
            client = chromadb.PersistentClient(path=chromaDbTeleports)
            collection = client.get_collection(collectionTeleport)

            # collection.delete(ids="2ef19a59-7f4c-43dd-a62e-82f692b57ea6")
            collection.delete(ids=ids)

            return True
        except:
            print('error')
    
    def getRevevantInfoFromDbForChat(self, chromaDbPath: str, collectionName: str):
        embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        db3 = Chroma(persist_directory=chromaDbPath, embedding_function=embedding_function, collection_name=collectionName)
        retriever = db3.as_retriever(search_type="similarity", search_kwargs = {"k": 3})

        return retriever
    

    def getRevevantInfoFromDb(self, chromaDbPath: str, collectionName: str):
        embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        db3 = Chroma(persist_directory=chromaDbPath, embedding_function=embedding_function, collection_name=collectionName)
        retriever = db3.as_retriever(search_type="similarity", search_kwargs = {"k": 10})

        return retriever

        # client = chromadb.PersistentClient(path=chromaDbPath)
        # collection = client.get_collection(collectionName)

        # results = collection.query(
        #     query_texts=[query],
        #     n_results=1
        # )

        # print(results)

        # print(collectionName)

        # return results['documents'][0][0]

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
                # print(f"Moved: {source_file} to {destination_file}")
            except Exception as e:
                print(f"Error moving {source_file} to {destination_file}: {e}")
    

    def create_teleport(self, collectionName, chats):

        print(f"CHATS: {chats}")
        print(f"COLLECTION_NAME {collectionName}")
        try:
            ids = []
            docs = []
            metadatas = []
            for chat in chats:
                myData = self.getDataFromChromaDb(self.chromaDbTeleportsPath, chat)

                print(myData)
                ids = ids + myData['ids']
                docs = docs + myData['documents']
                metadatas = metadatas + myData['metadatas']

            print(ids)
            print(docs)
            print(metadatas)


            client = chromadb.PersistentClient(path="your_database_path")

            # Create a new collection (replace "my_collection" with your desired collection name)
            newCollection = client.create_collection(collectionName)
            newCollection.add(ids=ids, documents=docs, metadatas=metadatas)

            return True
        
        except:
            return False
        
    
    def delete_chat_from_teleport():
        pass
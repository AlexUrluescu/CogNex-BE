


import os
from dotenv import load_dotenv
load_dotenv()

from langchain.vectorstores.chroma import Chroma
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings

from langchain.chat_models import AzureChatOpenAI
from langchain.chains import RetrievalQA

class AskChat():
    def __init__(self):
        self.OPENAI_API_TYPE = "azure"
        self.OPENAI_API_VERSION = os.environ.get("OPENAI_API_VERSION")
        self.OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
        self.OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE")
        self.OPENAI_API_VERSION = "2023-03-15-preview"

        # self.database = database
        # self.query = query

    
    def answering(self, database, query):
        embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")


        db3 = Chroma(persist_directory= database, embedding_function=embedding_function)


        retriever = db3.as_retriever()
        # relevant_docs = retriever.get_relevant_documents(self.query)
        # # print(relevant_docs)

        llm = AzureChatOpenAI(
            deployment_name = "gpt35-uif54579",
            model_name = "gpt-35-turbo",
            temperature = 0.7
        )

        chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever = retriever, return_source_documents = True)

        llm_response = chain(query)

        return llm_response['result']
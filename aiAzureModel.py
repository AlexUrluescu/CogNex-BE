
import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from langchain.vectorstores import AzureSearch
from langchain.chat_models import AzureChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain.text_splitter import TokenTextSplitter

load_dotenv()


# OPENAI_API_TYPE = "azure"
# # OPENAI_API_VERSION = os.environ.get("OPENAI_API_VERSION")
# OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
# OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE")
# OPENAI_API_VERSION = "2023-03-15-preview"

class AskAzure():
    def __init__(self):
        self.OPENAI_API_TYPE = "azure"
        self.OPENAI_API_VERSION = os.environ.get("OPENAI_API_VERSION")
        self.OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
        self.OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE")
        self.OPENAI_API_VERSION = "2023-03-15-preview"

        self.AZURE_COGNITIVE_SEARCH_INDEX_NAME = os.environ.get("AZURE_COGNITIVE_SEARCH_INDEX_NAME")
        self.AZURE_COGNITIVE_SEARCH_ENDPOINT = os.environ.get("AZURE_COGNITIVE_SEARCH_ENDPOINT")
        self.AZURE_COGNITIVE_SEARCH_SERVICE_NAME = os.environ.get("AZURE_COGNITIVE_SEARCH_SERVICE_NAME")

        self.AZURE_COGNITIVE_SEARCH_API_KEY = os.environ.get("AZURE_COGNITIVE_SEARCH_API_KEY")
        self.credential = AzureKeyCredential(self.AZURE_COGNITIVE_SEARCH_API_KEY)

    
    def answering(self, query):

        embeddings = OpenAIEmbeddings(
            deployment="adagptmodel",
            model="text-embedding-ada-002",
            openai_api_base=self.OPENAI_API_BASE,
            openai_api_type=self.OPENAI_API_TYPE,
        )

        acs = AzureSearch(azure_search_endpoint=self.AZURE_COGNITIVE_SEARCH_ENDPOINT ,
                azure_search_key=self.AZURE_COGNITIVE_SEARCH_API_KEY,
                index_name=self.AZURE_COGNITIVE_SEARCH_INDEX_NAME,
                embedding_function=embeddings.embed_query)

        llm = AzureChatOpenAI(deployment_name="gpt35-uif54579", openai_api_key=self.OPENAI_API_KEY, openai_api_base=self.OPENAI_API_BASE, openai_api_version=self.OPENAI_API_VERSION)


        CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template("""GIVEN THE FOLLOWING CONVERSATION AND A FOLLOW UP QUESTION,REPHRASE THE FOLLOW UP QUESTION TO BE STANDALONE QUESTION.
            Chat History:
            {chat_history}
            Follow up input:{question}
            Standalone question:""")

        qa = ConversationalRetrievalChain.from_llm(llm=llm, retriever=acs.as_retriever(), condense_question_prompt=CONDENSE_QUESTION_PROMPT,return_source_documents=True, verbose=False)

        chat_history = []

        result = qa({"question": query, "chat_history": chat_history})

        print(f"Question: {query}")

        print(f"Answer: {result}")

        return result["answer"]

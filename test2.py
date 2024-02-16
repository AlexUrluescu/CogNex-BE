# %% [markdown]
# ## This file get info already stored in chroma database (the best version)

# %% [markdown]
# ### Import the libraries to get the env variables

# %%
import os
from dotenv import load_dotenv

# %%
load_dotenv()

OPENAI_API_TYPE = "azure"
OPENAI_API_VERSION = os.environ.get("OPENAI_API_VERSION")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE")
OPENAI_API_VERSION = "2023-03-15-preview"

# %%
OPENAI_API_KEY 

# %%
# database = "./conventia_viena-database"
database = "C:/Users/Alex/OneDrive/Documente/PersonalRepos/AI/LangChain/AzureCognitiveSearch/conventia_viena-database"
query = "Cand intra un tratat in vigoare?'?"

# %% [markdown]
# ### Import the libraries to connect to chroma database

# %%
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings


# %%
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")


# %% [markdown]
# ##### Connect to chroma database

# %%
db3 = Chroma(persist_directory=database, embedding_function=embedding_function)


# %% [markdown]
# ##### Create the retriever and get relevant documents

# %%
retriever = db3.as_retriever()
relevant_docs = retriever.get_relevant_documents(query)

print(relevant_docs)

# %% [markdown]
# #### Import the model 3.5 turbo

# %%
from langchain.chat_models import AzureChatOpenAI
from langchain.chains import RetrievalQA

llm = AzureChatOpenAI(
    deployment_name = "gpt35-uif54579",
    model_name = "gpt-35-turbo",
    temperature = 0.7
)

# %%
llm

# # %%
chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever = retriever, return_source_documents = True)


# # %%
# def process_llm_response(llm_response):
#     print(llm_response['result'])
#     print("\n\nSources:")
#     for source in llm_response["source_documents"]:
#         print(source.metadata['source'])

# # %%
llm_response = chain(query)

# with open(llm_response['result'], "w", encoding="utf-8") as f:
    # f.write(html)

print(llm_response)

# # %%
# process_llm_response(llm_response)

# # %%
llm_response['result']




from aiModelClass import AskChat

database = "C:/Users/Alex/OneDrive/Documente/PersonalRepos/AI/LangChain/AzureCognitiveSearch/football-database"

a = AskChat()

answer = a.answering(database, "What was the first team where Cristiano Ronaldo played?")

print(answer)
from utils import Utils

utils = Utils()

docsPath = "./testing_personal_documents/"
chromaDbPath = "testing"

utils.storeDataIntoChroma(docsPath, chromaDbPath, 'test2')
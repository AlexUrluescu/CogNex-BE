from utils import Utils

utils = Utils()

docsPath = "./testing_personal_documents/"
chromaDbPath = "testing"

collection = '6612b895948177eb9ba4033c'

query = "Key skills of Messi?"

# utils.storeDataIntoChroma(docsPath, chromaDbPath, 'test2')
utils.getRevevantInfoFromDb(chromaDbPath, collection, query)


# Example usage:
# source_directory = "/Users/alexandreurluescu/Documents/current work/CogNex/CogNex-BE/server/users_documents2/65e46bd58d312e7ab5895adf"
# destination_directory = "/Users/alexandreurluescu/Documents/current work/CogNex/CogNex-BE/server/users_documents/65e46bd58d312e7ab5895adf"
# move_files(source_directory, destination_directory)
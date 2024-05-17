from Google import Create_Service

from google.oauth2 import service_account
from googleapiclient.discovery import build

CLIENT_SECRET_FILE = 'client_secret_GoogleCloud2.json'
API_NAME = 'drive'
API_VERSION = 'v3'
scope =["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
PARENT_FOLDER_ID = "1moLI5PhWexVLUjNGwQ00g7NVwtQWyP3P"

# service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, scope)

# national_parks = ['hei1', 'hei2', 'hei3']

# print(service)

# for nat_park in national_parks:
#     file_metadata = {
#         'name': nat_park,
#         'mimeType': 'application/vnd.google-apps.folder',
#         # 'parents': []
#     }

#     service.files().create(body=file_metadata).execute()


def auth():
    creds = service_account.Credentials.from_service_account_file(CLIENT_SECRET_FILE, scopes=scope)

    print(creds)
    return creds

def upload(filePath):
    creds = auth()

    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': "Messi",
        'parents': [PARENT_FOLDER_ID]
    }


    file = service.files().create(body=file_metadata, media_body=filePath).execute()

upload('testing_documents/Messi.pdf')
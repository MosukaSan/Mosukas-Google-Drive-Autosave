import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

class GoogleDriveService:
    def __init__(self):
        self.creds = None
        self.service = None

    def authenticate(self):
      SCOPES = ["https://www.googleapis.com/auth/drive.file"]
      
      if os.path.exists("token.json"):
        self.creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  
      if not self.creds or not self.creds.valid:
        if self.creds and self.creds.expired and self.creds.refresh_token:
          self.creds.refresh(Request())
        else:
          flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
          )
          self.creds = flow.run_local_server(port=0)
    
        with open("token.json", "w") as token:
          token.write(self.creds.to_json())

    def init_service(self):
       if self.creds is not None:
          self.service = build("drive", "v3", credentials=self.creds)
          return self.service
       else:
          print("You need to authenticate first")
      
    def create_folder(self, name: str):
      file_metadata = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder"
      }
        
      try:
        file = self.service.files().create(body=file_metadata, fields="id").execute()
        return file
      except HttpError as error:
        print(f"An error ocurred: {error}")
    
    def folder_exists(self, folder_id):
      try: 
        self.service.files().get(fileId=folder_id, fields="id, name").execute()
        return True
      except HttpError as error:
        print(error)
        return False

    def upload_file(self, name, location, folder):
      try:
        query = f"name = '{name}' and '{folder}' in parents"
        results = self.service.files().list(q=query, spaces="drive", fields="files(id, name)").execute()
        files = results.get("files", [])

        if files:
          media = MediaFileUpload(location, resumable=True)
          self.service.files().update(fileId=files[0]["id"], media_body=media).execute()
        else:
          file_metadata = {"name": name, "parents": [folder]}
          media = MediaFileUpload(location, resumable=True)
          self.service.files().create(body=file_metadata, media_body=media, fields="id").execute()
      except HttpError as error:
        print(error)

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os.path
import pickle

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_google_drive_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no valid credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credenciales.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)

def upload_file(filename):
    service = get_google_drive_service()
    
    file_metadata = {'name': filename}
    media = MediaFileUpload(filename,
                          mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    
    file = service.files().create(body=file_metadata,
                                media_body=media,
                                fields='id').execute()
    
    print(f'File ID: {file.get("id")}')
    return file.get('id')

# Example usage
excel_file = 'your_excel_file.xlsx'
file_id = upload_file(excel_file)
import os
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
SERVICE_ACCOUNT_FILE = "service-account.json"

def download_solutions():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    drive_service = build("drive", "v3", credentials=creds)

    folder_id = "YOUR_GOOGLE_DRIVE_FOLDER_ID"
    query = f"'{folder_id}' in parents and mimeType='text/plain'"
    
    results = drive_service.files().list(q=query).execute()
    files = results.get("files", [])

    for file in files:
        request = drive_service.files().get_media(fileId=file["id"])
        with open(f"solutions/{file['name']}", "wb") as f:
            f.write(request.execute())

if __name__ == "__main__":
    download_solutions()

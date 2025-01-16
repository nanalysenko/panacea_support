import os
import google.auth
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def retrieve_data(spreadsheet_id, range_name):
    """
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "/Users/analys/code/local_code/поддержка_ таблицы/test/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())



    try:
        service = build("sheets", "v4", credentials=creds)
        # Call sheets api
        result = (service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute())
        rows = result.get("values", [])
        print(f"{len(rows)} rows retrieved")
        return result
    except HttpError as error:
        print(f"An error occured: {error}")
        return error


if __name__ == "__main__":
    spread_sheet_id = '1B2ZhQtveFkxiOLT0dLcNsC9dKxnG99v5FlSFW4hjnRY'
    range_vals = "A1:B2"
    res = retrieve_data(spread_sheet_id, range_vals)
    print(res)
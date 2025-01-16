import os
import google.auth
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def post_data(spreadsheet_id, range_name, value_input_option, _values):
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
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    try: 
        service = build("sheets", "v4", credentials=creds)
        values = [[], ]
        body = {"values":_values}
        result = (service.spreadsheets().values().update(spreadsheetId=spreadsheet_id,
                                                           range=range_name,
                                                           valueInputOption=value_input_option,
                                                           body=body,).execute())
        print(f"{result.get('updatedCells')} cells updated.")
        return result
    except HttpError as error:
        print(f"An error occured {error}")
        return error

if __name__ == "__main__":
    spreadsheet_id = "1B2ZhQtveFkxiOLT0dLcNsC9dKxnG99v5FlSFW4hjnRY"
    cell_range = "A1:C4"
    value_input_option = "USER_ENTERED"
    post_data(spreadsheet_id, cell_range, value_input_option, [["A", "A"], ["l"]],)


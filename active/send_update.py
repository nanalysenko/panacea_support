# at the end of the day,
# check every table to find if there is new data for that day
# read data into json
# отправить обновление по клиникам девочкам в тг в конце дня# imports
import os
import json 
import pandas as pd
from datetime import datetime
import google.auth
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from functions import retrieve_data, post_data

SPREADSHEET_ID = '1AM-C5b9tfg1GA-y2-XKn0sPRS5_DPbjvXlV6ErK1agI'
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def get_sheet_names(spreadsheet_id):
    # Call the Sheets API
    sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    # Extract sheet names
    sheet_names = [sheet['properties']['title'] for sheet in sheet_metadata.get('sheets', [])]
    return sheet_names

def get_data_from_sheet(spreadsheet_id, sheet_name):
    # Define the range you want to read (e.g., 'Sheet1!A1:D10')
    range_name = f"{sheet_name}!A1:D10"  # Adjust the range as needed
    # Call the Sheets API
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range_name
    ).execute()
    values = result.get('values', [])
    return values


if __name__ == "__main__":
    creds = None

    # get list of tables 
    sheet_name = 'Таблицы по ОС для клиник'
    cell_range = 'A1:B1000'
    range_find = f"{sheet_name}!{cell_range}"
    res = retrieve_data(SPREADSHEET_ID, range_find)
    with open('active/data/sheet_names.json', 'w') as f:
        json.dump(res, f)

    # выгрузить из json список ссылок
    with open('active/data/sheet_names.json', 'r') as f:
        data = json.load(f)
    data_list = []
    for d in data['values']:
        if len(d) > 1: 
            if d[1].startswith('https:'): data_list.append(d)
    spread_sheet_ids = [val[1] for val in data_list]
    spread_sheet_ids = [val.split("/d/")[1].split("/")[0] for val in spread_sheet_ids]
    clinic_names = [val[0] for val in data_list]

    # get num of last non empty row in full table
    # table_id = '1AM-C5b9tfg1GA-y2-XKn0sPRS5_DPbjvXlV6ErK1agI'
    cell_range = 'A1:D'
    sheet_name = 'Учет обращений'
    range_find = f"{sheet_name}!{cell_range}"
    res2 = retrieve_data(SPREADSHEET_ID, range_find)['values']
    num_rows = len(res2)
    print(num_rows)


    # по всем айди выделить дату, если дата совпадает взять содержание
    for i in range(len(spread_sheet_ids)):
        id = spread_sheet_ids[i]
        sheet_name = 'ОС'
        cell_range = 'A1:G1000'
        range_find = f"{sheet_name}!{cell_range}"
        res = retrieve_data(id, range_find)['values']
        for row in res:
            try:
                if pd.to_datetime(row[0], format='%d.%m.%Y').date() == datetime.today().date():
                    # post this data to the full table
                    request = row[4]
                    clinic_name = clinic_names[i]
                    date_today = row[0].strip('.2025')
                    print([request, clinic_name, date_today])
                    # get last empty row - num_rows
                    # post
                    num_rows +=1
                    value_input_option = "USER_ENTERED"
                    cell_range = f'B{num_rows}:D'
                    sheet_name = 'Учет обращений' # изменить
                    range_post = f"{sheet_name}!{cell_range}"
                    post_data(SPREADSHEET_ID, range_post, value_input_option, [[request, clinic_name, date_today]],)
                    # print('lll')
            except:
                pass

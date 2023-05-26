import pickle
from pathlib import Path
from typing import Optional, Dict

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pandas as pd

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
REG_ID = "1Vmnts92YLwso_DWVnzYUvqz8Zkdhz_pXnkFXoWox348"
TAB_NAME = "submissions"
ROOT = Path(__file__).parents[1]


def gsheet_api_check():
    token_file = ROOT / 'token.pickle'
    cred_file = ROOT / 'credentials.json'
    creds = None
    if token_file.is_file():
        with token_file.open('rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(cred_file), SCOPES)
            creds = flow.run_local_server(port=0)
        with token_file.open('wb') as token:
            pickle.dump(creds, token)

    return creds


def pull_sheet_data(spread_sheet_id: str, tab_name: str):
    creds = gsheet_api_check()
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=spread_sheet_id,
        range=tab_name).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        rows = sheet.values().get(spreadsheetId=spread_sheet_id,
                                  range=tab_name).execute()
        data = rows.get('values')
        print("COMPLETE: Data copied")
        return data


def refresh_registry():
    data = pull_sheet_data(REG_ID, TAB_NAME)
    df = pd.DataFrame(data[1:], columns=data[0])
    df.to_csv(ROOT / "data/registry.csv")


def load_registry_as_csv() -> Optional[pd.DataFrame]:
    if not (ROOT / 'data/registry.csv').is_file():
        return None
    df = pd.read_csv(ROOT / 'data/registry.csv')
    df.rename(columns={df.columns[0]: "index"}, inplace=True)
    return df


def load_registry_as_dict() -> Optional[Dict]:
    df = load_registry_as_csv()
    if df is None:
        return None

    data = df.to_dict(orient="records")
    return {
        f"{row['model_id']}": row
        for row in data
    }

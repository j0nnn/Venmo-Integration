from __future__ import print_function
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials.json'

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)


# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1GS1vMOKHn0Su2p76OWi6EYxCKCs7DKTQG-3ij3tEU58'
RANGE = "Fundraisers!A4:D200"

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=RANGE).execute()
values = result.get('values', [])

temp = [["a", 1, 2, 3], ["b", 4, 5, 6]]

request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=RANGE, valueInputOption="RAW", body={"values":temp})
request.execute()

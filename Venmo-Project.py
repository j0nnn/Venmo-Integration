from venmo_api import Client
from dotenv import load_dotenv
import os
import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account

load_dotenv()
user = os.getenv("user")
pwd = os.getenv("pwd")
access_token = os.getenv('access_token')
tasa_id = os.getenv('tasa_id')
jon_id = os.getenv('jon_id')

#access_token = Client.get_access_token(username=user, password=pwd)

# Initialize api client using an access-token
client = Client(access_token=access_token)

# Helper function that compares two Date objects
def compareDate(date1, date2):
    if (date1 < date2):
        return -1
    elif (date1 > date2):
        return 1
    else:
        return 0

# Getting Date Object from UTC
def getDatefromUTC(utc):
    return datetime.date.fromtimestamp(utc)


### VENMO DATA SEARCH ###


output = []
trans = client.user.get_user_transactions(user_id = tasa_id) #leo_id)
date_start = datetime.date(2021, 8, 1)
date_end = datetime.date(2021, 9, 1)
print("Transactions between", date_start, "and", date_end)
while trans.get_next_page() != None and compareDate(getDatefromUTC(trans[0].date_created), date_start) >= 0:
    for t in trans:
        t_date = getDatefromUTC(t.date_created)
        if t.target.display_name == "TASA Berkeley" and compareDate(t_date, date_start) >= 0 and compareDate(t_date, date_end) <= 0:
            space0 = ""
            space1 = ""
            space2 = ""
            for i in range(14 - len(t.actor.display_name[:14])):
                space0 += " "
            for i in range(34 - len(t.actor.display_name[:14]) - len(t.target.display_name) - len(" -> ") - len(space0)):
                space1 += " "
            for i in range(5 - len(str(t.amount))):
                space2 += " "
            print(t.actor.display_name[:14], space0, " -> ", t.target.display_name, space1, "date:", t_date.strftime("%m/%d/%Y"), "$:", t.amount, space2, "note:", t.note[0:30])
    trans = trans.get_next_page()
    #print("got new page")
output.reverse()


### GOOGLE SHEETS WRITE ###


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials.json'

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)


# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1GS1vMOKHn0Su2p76OWi6EYxCKCs7DKTQG-3ij3tEU58'
RANGE = "Fundraisers!A4:E200"

service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=RANGE, valueInputOption="RAW", body={"values":output})
request.execute()

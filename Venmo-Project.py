from venmo_api import Client
from dotenv import load_dotenv
import os
import datetime as dt
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Load credentials from environment variables
load_dotenv()
user = os.getenv("user")
pwd = os.getenv("pwd")
tasa_id = os.getenv('tasa_id')
access_token = os.getenv('tasa_access_token')
#access_token = Client.get_access_token(username=user, password=pwd)

# Initialize api client using access-token
client = Client(access_token=access_token)

# Helper function that compares two Date Objects
def compareDate(date1, date2):
    if (date1 < date2):
        return -1
    elif (date1 > date2):
        return 1
    else:
        return 0

# Helper function that converts UTC string to Date Object
def UTCtoDate(utc):
    return dt.date.fromtimestamp(utc)

# Helper function that converts input string (MM-DD-YYYY) to Date Object
def STRtoDate(str):
    return dt.datetime.strptime(str, '%m-%d-%Y').date()

### VENMO DATA SEARCH ###

# Returns set of transactions within date_start and date_end
output = []
transactions = client.user.get_user_transactions(user_id = tasa_id)

# Gets date from *args if valid, from user if not, defaults current month
date_end = dt.datetime.now().date()
date_start = dt.date(date_end.year, date_end.month, 1)
try:
    if (len(sys.argv) >= 3):
        date_start = STRtoDate(sys.argv[1])
        date_end = STRtoDate(sys.argv[2])
    else:
        date_start = STRtoDate(input('Start Date (MM-DD-YYYY): '))
        date_end = STRtoDate(input('End Date (MM-DD-YYYY): '))
except ValueError:
    print("Error: Invalid Date")

while (transactions.get_next_page() != None and
        compareDate(UTCtoDate(transactions[0].date_created), date_start) >= 0):
    for t in transactions:
        t_date = UTCtoDate(t.date_created)
        if (t.target.display_name == "TASA Berkeley" and
            compareDate(t_date, date_start) >= 0 and compareDate(t_date, date_end) <= 0):
            output.append([t_date.strftime("%m/%d/%Y"), t.note, t.actor.display_name, t.amount, t.actor.username])
    transactions = transactions.get_next_page() # maximum 50 results per page
output.reverse()



### GOOGLE SHEETS WRITE ###


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials.json'

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)


# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1GS1vMOKHn0Su2p76OWi6EYxCKCs7DKTQG-3ij3tEU58'
RANGE = "Fundraisers!A4:E1000"

service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=RANGE, valueInputOption="RAW", body={"values":output})
request.execute()

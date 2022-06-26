from venmo_api import Client
from dotenv import load_dotenv
import os
import sys
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

# Bottleneck of speed; reduce API calls (get_next_page) in conditionals/loops
def getFirstDate():
    transactions = client.user.get_user_transactions(user_id = tasa_id)
    while transactions.get_next_page().get_next_page() != None:
        transactions = transactions.get_next_page()
    return UTCtoDate(transactions[-1].date_created)

# firstDate = getFirstDate();
firstDate = dt.date(2020, 1, 2) # Unique to TASA Berkeley account

### VENMO DATA SEARCH ###

# Returns set of transactions within date_start and date_end, match keyword
def transactionSearch(date_start, date_end, keyword):
    output = []
    transactions = client.user.get_user_transactions(user_id = tasa_id)

    # checks if date range is not before first Transaction date
    if compareDate(date_start, firstDate) < 0:
        date_start = firstDate
    if compareDate(date_end, firstDate) < 0:
        date_end = firstDate

    # NOTE: pages are in reverse chronological order

    print("flag: skipping pages")
    while compareDate(UTCtoDate(transactions[-1].date_created), date_end) > 0:
        # maximum 50 results per page, len(transactions) = 37 tho?
        transactions = transactions.get_next_page()

    print("flag: starting filtering")
    while compareDate(UTCtoDate(transactions[0].date_created), date_start) >= 0:
        for t in transactions:
            t_date = UTCtoDate(t.date_created)
            if (t.target.display_name == "TASA Berkeley" and
                compareDate(t_date, date_start) >= 0):
                if keyword:
                    if keyword in t.note.lower():
                        output.append([t_date.strftime("%m/%d/%Y"), t.note, t.actor.display_name, t.amount, t.actor.username])
                else:
                    output.append([t_date.strftime("%m/%d/%Y"), t.note, t.actor.display_name, t.amount, t.actor.username])
        transactions = transactions.get_next_page() # maximum 50 results per page
    output.reverse()
    return output

if __name__ == "__main__":
    # Gets date from *args, if valid, from user; if not, defaults current month
    date_end = dt.datetime.now().date()
    date_start = dt.date(date_end.year, date_end.month, 1)
    keyword = ""

    try:
        if (len(sys.argv) >= 3):
            date_start = STRtoDate(sys.argv[1])
            date_end = STRtoDate(sys.argv[2])
        else:
            date_start = STRtoDate(input('Start Date (MM-DD-YYYY): '))
            date_end = STRtoDate(input('End Date (MM-DD-YYYY): '))
    except ValueError:
        print("Error: Invalid Date")
    keyword = input('Keyword: ').lower()

    output = transactionSearch(date_start, date_end, keyword)
    for transaction in output:
        print(transaction)

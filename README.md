# Venmo-Spreadsheet Integration
In this project we created a program that utilizes the RESTful API of Venmo and Google Sheets. This would automate the transfer of budgetary information such as money recieved from fundraisers, money spent, etc..

We are considering making this a web-app so that it would be accessible to everyone, but for now, all private authentication processes run within the code.

The credentials.json file contains information about the Google Sheets API. If you want to pull from the repository, you would need to have your own json file. Please contact us help getting the neccessary files.

Installing required packages (stored in ./requirements.txt):
pip install -r requirements.txt

Instructions to run are contained in the Makefile (2 main commands):
```
make venv
make run
```

NOTE: as of 2024 (maybe earlier), Venmo Developer APIs were retired, so unfortunately, the tool can no longer be used.

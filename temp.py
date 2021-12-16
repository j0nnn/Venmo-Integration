from venmo_api import Client
from pprint import pprint
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
user = os.getenv("user")
pwd = os.getenv("pwd")
access_token = os.getenv('access_token')
tasa_id = os.getenv('tasa_id')
jon_id = os.getenv('jon_id')

# Get your access token. You will need to complete the 2FA process
# Please store it somewhere safe and use it next time
# Never commit your credentials or token to a git repository

# access_token = Client.get_access_token(username='email', password='password')
# print("My token:", access_token)

# Initialize api client using an access-token
client = Client(access_token=access_token)

# Search for users. You get a maximum of 50 results per request.
#users = client.user.search_for_users(query="TASA-Berkeley")
#users = client.user.search_for_users(query="jonathansun63")
#for user in users:
#    pprint(user.to_json())

# Or pass a callback to make it multi-threaded
#def callback(users):
#    for user in users:
#        print(user.username)
#client.user.search_for_users(query="TASA-Berkeley", callback=callback, limit=10)

#payment_methods = client.payment.get_payment_methods()
#for method in payment_methods:
#    pprint(method.to_json())
#client.payment.request_money(100, "i like money", jon_id)
#client.payment.send_money(0, "you like money", jon_id)

#trans = client.user.get_user_transactions(user_id = jon_id, limit=1)
#for t in trans:
#    print(t.actor.display_name, " -> ", t.target.display_name, "audience: ", t.audience, "note: ", t.note)
#    pprint(t.to_json())

#friend = client.user.get_user_friends_list(user_id = jon_id)
#for friend in friends:
#    print(friend.username)

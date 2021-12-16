from venmo_api import Client

# Get your access token. You will need to complete the 2FA process
# Please store it somewhere safe and use it next time
# Never commit your credentials or token to a git repository

# access_token = Client.get_access_token(username='email', password='password')
# print("My token:", access_token)

access_token = "access_token"

# Initialize api client using an access-token
client = Client(access_token=access_token)

# Search for users. You get a maximum of 50 results per request.
users = client.user.search_for_users(query="Peter")
for user in users:
   print(user.username)

# Or pass a callback to make it multi-threaded
def callback(users):
   for user in users:
       print(user.username)

client.user.search_for_users(query="peter",
                            callback=callback,
                            limit=10)

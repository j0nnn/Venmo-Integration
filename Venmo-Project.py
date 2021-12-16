from venmo_api import Client

# Get your access token. You will need to complete the 2FA process
# Please store it somewhere safe and use it next time
# Never commit your credentials or token to a git repository
                                  
# Initialize api client using an access-token
client = Client(access_token="806a651ec53d2b8b8e28090bd1114aee6920a0cd748e4ee1b8bfd0258582f529")

bruh = client.user.get_user_transactions(user_id = "3186573273202688541")
for lmao in bruh:
    print(lmao.actor.display_name, " -> ", lmao.target.display_name)
#2912360473821184765


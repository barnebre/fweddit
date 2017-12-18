import time
from datetime import datetime
from esipy import App
from esipy import EsiClient
from esipy import EsiSecurity
# required stuff
# 1- the app
App = App.create('https://esi.tech.ccp.is/latest/swagger.json?datasource=tranquility')

# 2- the security object, that knows your clientid/secret
EsiSecurity = EsiSecurity(
    app=App,
    redirect_uri='https://localhost/callback/',
    client_id='***',
    secret_key='***'
)

# 3- A client that knows what security object he can use (if None specified, it'll use none)
EsiClient = EsiClient(
    security = EsiSecurity,
    header = {'User-Agent': 'Always set this with something CCP can use to contact you'},
)
refresh_token = "Your Actual Refresh Token"

# two way of doing this, both work, the 2nd have less risks to fail if I change anything one day

# 1. using the attribute
EsiSecurity.refresh_token = refresh_token

# 2. using the update_token method
# this method actually take a dict with the same format you get from auth.eveonline.com/oauth/token
EsiSecurity.update_token({
    'access_token': 'can be empty, does not matter',
    'expires_in': -1,  # any number works, but -1 will force refreshing access token if you don't do it manually 
    'refresh_token': refresh_token,
})

# now you gave the security all data it needs, let's get the new tokens
# EsiSecurity.refresh() already updates itself with the new tokens
new_tokens = EsiSecurity.refresh()
# verify, get the data from the authed char
verify = EsiSecurity.verify()
character_id = verify['CharacterID']
character_name = verify['CharacterName']

# init the operation you want to call
wallet = App.op['get_characters_character_id_wallets'](
    character_id=character_id
)

# do the actual request. EsiClient.request() will add the required headers using the 
# security object we gave him at the beginning
walletdata = EsiClient.request(wallet)

print("%s balance : %0.2f ISKs" % (
    character_name,
    wallet.data[0].balance / 100.0
))
# -------------------------------------
# SAVING THE TOKENS
# -------------------------------------    

# if you are refreshing
new_tokens = EsiSecurity.refresh()
# if you are coming from auth
new_tokens = EsiSecurity.auth(code_from_auth)

# this is what you **need** to save
access_token = new_tokens['access_token']
refresh_token = new_tokens['refresh_token']

# for expire, you need to save the real date
expire_date = datetime.fromtimestamp(
    time.time() + new_tokens['expires_in'],
)

# now save it the way you want.

# -------------------------------------
# LOADING FROM YOUR SAVE
# -------------------------------------
# load the data from your save, then :
EsiSecurity.update_token({
    'access_token': access_token,
    'expires_in': expire_date - datetime.utcnow(), #<-- this is important
    'refresh_token': refresh_token,
})

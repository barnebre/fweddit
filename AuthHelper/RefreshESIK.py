import webbrowser
import csv
import re
import urllib
from esipy import EsiSecurity
from esipy import App
from esipy import EsiClient
from esipy import EsiSecurity

import sys
sys.path.append('/home/pi/new-rgb/rpi-rgb-led-matrix-master')


#Load type_id for Eve type names

reader = csv.reader(open('/home/pi/typeid2.csv'))


#This is for type_id.csv, create dictionary

result = {}
for row in reader:
    key = row[0]
    if key in result:
        # implement your duplicate row handling here
        pass
    result[key] = row[1:]

#This is for number layout later

def intWithCommas(x):
    if type(x) not in [type(0)]:
        raise TypeError("Parameter must be an integer.")
    if x < 0:
        return '-' + intWithCommas(-x)
    result = ''
    while x >= 1000:
        x, r = divmod(x, 1000)
        result = ",%03d%s" % (r, result)
    return "%d%s" % (x, result)


#Print your last access token from file.py

print (file.acc)


#Standard stuff for Authentication

esi_app = App.create('https://esi.tech.ccp.is/latest/swagger.json?datasource=tranquility')

esi_security = EsiSecurity(
                app=esi_app,
                redirect_uri='https://localhost/callback/',
                client_id='***',
                secret_key='***'
)


uri = esi_security.get_auth_uri(scopes=['esi-wallet.read_character_wallet.v1'])

esi_client = EsiClient(esi_security)


# Create response header to load afterwards back

header_re = {
     "access_token": '%s' % file.acc,
     "token_type":"Bearer",
     "expires_in": int(file.exp_t_s),
     "refresh_token":"***static***"
    }

#This was for authentication to generate auth-code to get access token

#print uri
#x=raw_input("Paste Code :")
#esi_security.auth(x)
#verify=esi_security.verify()


#Important stuff, load response header to upload "token" and refresh to get new access token, last verify to get your needed inquiry response

esi_security.update_token(header_re)
esi_security.refresh()
verify=esi_security.verify()


#Get access token and time token from esipy code after successful refresh (expiry method is custom changed)
accesscode = esi_security._EsiSecurity__get_token_auth_header()
accesscode = accesscode['Authorization'][8:]
timestp = esi_security.is_token_expired2() #custom changed


#Writing access token from refresh token use and timestamp to file for later use in when calling this script
f = open( 'file.py', 'w' ) 
f.write( 'acc = ' + repr(accesscode) + '\n' )
f.write( 'exp_t_s = ' + str(timestp*(-1)) + '\n' )
f.close()



#The following is processing and your required data inquiry from ESI network

myid = verify['CharacterID']
myname = verify['CharacterName']

wallet = esi_app.op['get_characters_character_id_wallets'](
character_id =myid

        )
walletdata = esi_client.request(wallet)

#Present output


print "%s's ISK:" % (myname)
print (intWithCommas(int(float(walletdata.data[0]['balance'])/100)))

#Optional, use dictionary for idcheck = "type_id in question"

#print  result[str(idcheck)][0]
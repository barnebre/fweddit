'''import asyncio
import logging
import operator
import re
import shelve
import datetime
from html.parser import HTMLParser
from time import sleep
import requests
import socket
from esipy import EsiClient, App

ALLIANCE = 1900696668
# ALLIANCE = 99002172
# ALLIANCE = 1354830081
global gameactive
gameactive = False

FIT_PARSE = re.compile('\[.+?, .+]')
OSMIUM_URL = 'https://o.smium.org/api/json/loadout/eft/attributes/loc:ship,a:tank,a:ehpAndResonances,a:capacitors,a:damage,a:priceEstimateTotal?input={}'
app = App.create(url="https://esi.tech.ccp.is/latest/swagger.json?datasource=tranquility")
client = EsiClient(
    retry_requests=True,  # set to retry on http 5xx error (default False)
    header={'User-Agent': 'Something CCP can use to contact you and that define your app'},
    raw_body_only=False  # default False, set to True to never parse response and only return raw JSON string content.
)
market_order_operation = app.op['get_markets_region_id_orders'](
    region_id=10000002,
    type_id=34,
    order_type='all'
)

# do the request
response = client.request(market_order_operation)
print (response.data[0].price)
'''
from AuthHelper.Mail import SendMail

'''from eve import Eve
from eve.auth import TokenAuth
from flask import current_app as app

class TokenAuth(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        """For the purpose of this example the implementation is as simple as
        possible. A 'real' token should probably contain a hash of the
        username/password combo, which sould then validated against the account
        data stored on the DB.
        """
        # use Eve's own db driver; no additional connections/resources are used
        accounts = app.data.driver.db['accounts']
        return accounts.find_one({'token': token})


if __name__ == '__main__':
    app = Eve(auth=TokenAuth)
    app.run()
    '''
from pyswagger import App
from esipy import EsiClient
from esipy import EsiSecurity
from datetime import datetime
import time
class ESILogger():
    def __init__(self):
        self.app = App.create(url="https://esi.tech.ccp.is/latest/swagger.json?datasource=tranquility")
    
    # replace the redirect_uri, client_id and secret_key values
    # with the values you get from the STEP 1 !
    def ESIMail(self,KilledCharID):
        security = EsiSecurity(
            app=self.app,
            redirect_uri='http://localhost/callback/',
            client_id='e84f425296ff43e7961f7ff677cd69fd',
            secret_key='dEcstK5mApwI2Rtj7TfhvZbIeH0yQvYQ5QNiyhBd',
        )
        
        # and the client object, replace the header user agent value with something reliable !
        client = EsiClient(
            retry_requests=True,
            header={'User-Agent': ''},
            security=security
        )
        print (security.get_auth_uri(scopes=['characterAccountRead','esi-mail.organize_mail.v1','esi-mail.read_mail.v1','esi-mail.send_mail.v1','esi-characters.read_contacts.v1']))
        try:
            tokens = security.auth('LzHL1UPo6bC5onVQfuhFRgVHki-Js6Sgk9sE0YaepHOPuK-PCp0sz3385LUonEc30')
        except:
            security.refresh_token="kmsk3RLruON523rwGEgyxDZBPH7MvddoN4wAEerZzoQ5ZozAJocXIm9H5DqxQ3Ik0"
            tokens = security.refresh()
        accessToken = tokens["access_token"]
        RefreshToken = tokens["refresh_token"]
        expire_date = datetime.fromtimestamp(time.time() + tokens['expires_in'],)
        api_info = security.verify()
        strCharacterID=api_info['CharacterID']
        Response = SendMail(strCharacterID, KilledCharID, "You got killed by <font size=\"12\" color=\"#ffffa600\"><a href=\"showinfo:2//98114328\">Fweddit!!!</a></font><font size=\"12\" color=\"#bfffffff\"></font>, you should join us!!! Be a ninja chicken today! See <font size=\"12\" color=\"#bfffffff\"></font><font size=\"12\" color=\"#ffffa600\"><loc><a href=\"https://j4lp.space/forums/viewtopic.php?f=15&t=215\">NinjaChicken</a></loc></font><font size=\"12\" color=\"#bfffffff\"></font>", accessToken)
        if Response.status_code == 201:
            print("Sent message to characterid {0}".format(KilledCharID))
if __name__ == '__main__':
    ESIMAIL = ESILogger()
    ESIMAIL.ESIMail(2113570501)
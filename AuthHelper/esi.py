from AuthHelper.Mail import SendMail
from pyswagger import App
from esipy import EsiClient
from esipy import EsiSecurity
from datetime import datetime
import time
CCPESIURL = "https://esi.tech.ccp.is/latest/swagger.json?datasource=tranquility"
CLIENTID = "e84f425296ff43e7961f7ff677cd69fd"
SECRETKEY = "dEcstK5mApwI2Rtj7TfhvZbIeH0yQvYQ5QNiyhBd"
REQUESTSCOPES = ['characterAccountRead','esi-mail.organize_mail.v1','esi-mail.read_mail.v1','esi-mail.send_mail.v1','esi-characters.read_contacts.v1']
CHARAUTHTOKEN = "LzHL1UPo6bC5onVQfuhFRgVHki-Js6Sgk9sE0YaepHOPuK-PCp0sz3385LUonEc30"
CHARREFRESHTOKEN = "kmsk3RLruON523rwGEgyxDZBPH7MvddoN4wAEerZzoQ5ZozAJocXIm9H5DqxQ3Ik0"
DEFAULTMESSAGE = "You got killed by <font size=\"12\" color=\"#ffffa600\"><a href=\"showinfo:2//98114328\">Fweddit</a></font><font size=\"12\" color=\"#bfffffff\"></font>, you should join us! Be a ninja chicken today! See <font size=\"12\" color=\"#bfffffff\"></font><font size=\"12\" color=\"#ffffa600\"><loc><a href=\"https://j4lp.space/forums/viewtopic.php?f=15&t=215\">NinjaChicken</a></loc></font><font size=\"12\" color=\"#bfffffff\"></font>"
TOKENAUTHKEY = "access_token"
TOKENREFRESHKEY = "refresh_token"
TOKENEXPIRESKEY = "expires_in"
SUCCESSRESPONSECODE = 201
class ESILogger():
    def __init__(self):
        self.app = App.create(url=CCPESIURL)
    
    # replace the redirect_uri, client_id and secret_key values
    # with the values you get from the STEP 1 !
    def ESIMail(self,KilledCharID):
        security = EsiSecurity(
            app=self.app,
            redirect_uri='http://localhost/callback/',
            client_id=CLIENTID,
            secret_key=SECRETKEY,
        )
        
        # and the client object, replace the header user agent value with something reliable !
        client = EsiClient(
            retry_requests=True,
            header={'User-Agent': ''},
            security=security
        )
        print (security.get_auth_uri(scopes=REQUESTSCOPES))
        try:
            tokens = security.auth(CHARAUTHTOKEN)
        except:
            security.refresh_token = CHARREFRESHTOKEN
            tokens = security.refresh()
        accessToken = tokens[TOKENAUTHKEY]
        RefreshToken = tokens[TOKENREFRESHKEY]
        expire_date = datetime.fromtimestamp(time.time() + tokens[TOKENEXPIRESKEY],)
        api_info = security.verify()
        strCharacterID=api_info['CharacterID']
        Response = SendMail(strCharacterID, KilledCharID, DEFAULTMESSAGE, accessToken)
        if Response.status_code == SUCCESSRESPONSECODE:
            print("Sent message to characterid {0}".format(KilledCharID))
if __name__ == '__main__':
    ESIMAIL = ESILogger()
    ESIMAIL.ESIMail(2113570501)
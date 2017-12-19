from AuthHelper.Mail import SendMail
from pyswagger import App
from esipy import EsiClient,EsiSecurity
from datetime import datetime
import time
from AuthHelper import Globals
class ESILogger():
    def __init__(self):
        self.app = App.create(url=Globals.CCPESIURL)
    def ESIMail(self,KilledCharID):
        security = EsiSecurity(
            app=self.app,
            redirect_uri='http://localhost/callback/',
            client_id=Globals.CLIENTID,
            secret_key=Globals.SECRETKEY,
        )
        
        client = EsiClient(
            retry_requests=True,
            header={'User-Agent': ''},
            security=security
        )
        print (security.get_auth_uri(scopes=Globals.REQUESTSCOPES))
        try:
            tokens = security.auth(Globals.CHARAUTHTOKEN)
        except:
            security.refresh_token = Globals.CHARREFRESHTOKEN
            tokens = security.refresh()
        accessToken = tokens[Globals.TOKENAUTHKEY]
        RefreshToken = tokens[Globals.TOKENREFRESHKEY]
        expire_date = datetime.fromtimestamp(time.time() + tokens[Globals.TOKENEXPIRESKEY],)
        api_info = security.verify()
        strCharacterID=api_info['CharacterID']
        Response = SendMail(strCharacterID, KilledCharID, Globals.DEFAULTMESSAGE, accessToken)
        if Response.status_code == Globals.SUCCESSRESPONSECODE:
            print("Sent message to characterid {0}".format(KilledCharID))
if __name__ == '__main__':
    ESIMAIL = ESILogger()
    ESIMAIL.ESIMail(2113570501)
from AuthHelper.Mail import SendMail
from pyswagger import App
from esipy import EsiClient,EsiSecurity
from datetime import datetime
import time
from AuthHelper import GlobalConsts
class ESILogger():
    def __init__(self):
        self.app = App.create(url=GlobalConsts.CCPESIURL)
    def ESIMail(self,KilledCharID):
        security = EsiSecurity(
            app=self.app,
            redirect_uri='http://localhost/callback/',
            client_id=GlobalConsts.CLIENTID,
            secret_key=GlobalConsts.SECRETKEY,
        )
        print (security.get_auth_uri(scopes=GlobalConsts.REQUESTSCOPES))
        try:
            tokens = security.auth(GlobalConsts.CHARAUTHTOKEN)
        except:
            security.refresh_token = GlobalConsts.CHARREFRESHTOKEN
            tokens = security.refresh()
        accessToken = tokens[GlobalConsts.TOKENAUTHKEY]
        RefreshToken = tokens[GlobalConsts.TOKENREFRESHKEY]
        expire_date = datetime.fromtimestamp(time.time() + tokens[GlobalConsts.TOKENEXPIRESKEY],)
        api_info = security.verify()
        strCharacterID=api_info['CharacterID']
        Response = SendMail(strCharacterID, KilledCharID, GlobalConsts.DEFAULTMESSAGE, accessToken)
        if Response.status_code == GlobalConsts.SUCCESSRESPONSECODE:
            print("Sent message to characterid {0}".format(KilledCharID))
        else:
            print("Failed to send message to characterid {0}".format(KilledCharID))
if __name__ == '__main__':
    ESIMAIL = ESILogger()
    ESIMAIL.ESIMail(2113570501)
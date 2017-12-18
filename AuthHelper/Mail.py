'''
Created on Dec 16, 2017

@author: Brent
'''
import requests
import simplejson
strMailURL="https://esi.tech.ccp.is/latest/characters/{0}/mail/?datasource=tranquility&token={1}"
def SendMail(strCharacterID,strRecipientId,strMessage,strToken):
    dictPayload = {
      "recipients": [
        {
          "recipient_type": "character",
          "recipient_id": 0
        }
      ],
      "subject": "Fweddit is recruiting!",
      "body": "string",
      "approved_cost": 0
    }
    dictPayload["recipients"][-1]["recipient_id"] = strRecipientId
    dictPayload["body"] = strMessage
    strMailCharURL = strMailURL.format(strCharacterID,strToken)
    return requests.post(strMailCharURL,data=simplejson.dumps(dictPayload))
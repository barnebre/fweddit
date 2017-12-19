'''
Created on Dec 18, 2017

@author: Brent
'''
import requests
from AuthHelper import GlobalConsts
import datetime
class CharESIError(Exception):
    def __init__(self,Error):
        super(CharESIError,self).__init__(Error)
def GetChar(CharacterID):
    CharInfo = requests.get(GlobalConsts.ESIGETCHARINFO.format(CharacterID)).json()
    return CharEsi(CharInfo,CharacterID)
class CharEsi():
    def __init__(self,CharESIInfo,charID):
        if('error' in CharESIInfo):
            raise CharESIError(CharESIInfo['error'])
        self.strBirthdate = CharESIInfo['birthday']
        self.strCharID = charID
        self.dtBirthdate = datetime.date(*[int(item) for item in self.strBirthdate.split('T')[0].split('-')])
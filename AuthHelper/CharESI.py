'''
Created on Dec 18, 2017

@author: Brent
'''
import requests
import simplejson
from AuthHelper import Globals
import datetime

def GetChar(CharacterID):
    CharInfo = requests.get(Globals.ESIGETCHARINFO.format(CharacterID)).json()
    return CharEsi(CharInfo,CharacterID)
class CharEsi():
    def __init__(self,CharESIInfo,charID):
        self.strBirthdate = CharESIInfo['birthday']
        self.strCharID = charID
        self.dtBirthdate = datetime.date(*[int(item) for item in self.strBirthdate.split('T')[0].split('-')])
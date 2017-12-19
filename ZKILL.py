'''
Created on Dec 16, 2017

@author: Brent
'''
import logging
import datetime
from AuthHelper import esi,CharESI,Globals
from threading import Thread
class Kill():
    def __init__(self, rawkill):
        self.killid = rawkill['package']['killID']
        self.attackers = rawkill['package']['killmail']['attackers']
        self.victim = rawkill['package']['killmail']['victim']
        self.value = rawkill['package']['zkb']['totalValue']
        self.shipID = self.victim['ship_type_id']
    def isKillCapsule(self):
        if self.shipID == 670 or self.shipID == 33328:
            return True
        return False
    def VictimInFweddit(self):
        if self.victim['corporation_id']== Globals.CORPORATIONID:
            return True
        else:
            return False
    def attackerInFweddit(self):
        if (len(self.attackers) > 100):
            return False
        for attacker in self.attackers:
            if 'corporation_id' in attacker:
                if attacker['corporation_id'] == Globals.CORPORATIONID:
                    return True
        return False

    def isOldKill(self):
        return self.killtime < datetime.datetime.now() - datetime.timedelta(hours=12)
def RecentLastKill(CharID):
    try:
        zkill = requests.get("https://zkillboard.com/api/kills/characterID/{}/".format(CharID), timeout=5)
        zkill = zkill.json()
        lastkill = datetime.date(*[int(item) for item in zkill[0]['killmail_time'].split('T')[0].split('-')])
        if(lastkill > (datetime.datetime.now() - datetime.timedelta(days=7)).date()):
            return True
        else:
            return False
    except:
        return False
    
def CheckKillMail(killRec):
    if killRec.isKillCapsule():
        return
    if killRec.VictimInFweddit():
        print("Victim in fweddit")
        logging.info("Victim in fweddit")
        return
    if not killRec.attackerInFweddit():
        return
    charVict = CharESI.GetChar(killRec.victim['character_id'])
    if(not RecentLastKill(charVict.strCharID)):
        return
    if(charVict.dtBirthdate > (datetime.datetime.now() - datetime.timedelta(days=365)).date()):
        return
    print("Sending message to {0}".format(charVict.strCharID))
    logging.info("Sending message to {0}".format(charVict.strCharID))
    ESIHandler.ESIMail(charVict.strCharID)
    
if __name__ == '__main__':
    import requests
    print("running...")
    logging.info("running...")
    ESIHandler = esi.ESILogger()
    while True:
        r = requests.get('https://redisq.zkillboard.com/listen.php').json()
        if r:
            try:
                killReq = Kill(r)
            except TypeError:
                continue
        #Maybe thread later to catch all kills, zkill call in check kill mail can take some time allowing kills to be missed
        #Thread(target= CheckKillMail(killReq))
        CheckKillMail(killReq)
        
            
            

'''
Created on Dec 16, 2017

@author: Brent
'''

ALLIANCE = 1900696668
CORPORATIONID = 98114328
# ALLIANCE = 99002172
#ALLIANCE = 1354830081
import logging
from datetime import datetime
import dateutil.parser
from AuthHelper import esi
class Kill():
    def __init__(self, rawkill):
        self.killid = rawkill['package']['killID']
        self.killtime = dateutil.parser.parse(rawkill['package']['killmail']['killmail_time'])#, 'YYYY-MM-DDTHH:mm:ssZ')
        self.attackers = rawkill['package']['killmail']['attackers']
        self.victim = rawkill['package']['killmail']['victim']
        self.value = rawkill['package']['zkb']['totalValue']

    def VictimInFweddit(self):
        if self.victim['corporation_id']== CORPORATIONID:
            return True
        else:
            return False
    def attackerInFweddit(self):
        for attacker in self.attackers:
            if 'corporation_id' in attacker:
                if attacker['corporation_id'] == CORPORATIONID:
                    return True
        return False

    def isOldKill(self):
        return self.killtime < datetime.now + datetime.timedelta(hours=12)

if __name__ == '__main__':
    import requests
    print("running...")
    logging.info("running...")
    ESIMailer = esi.ESILogger()
    while True:
        r = requests.get('https://redisq.zkillboard.com/listen.php').json()
        if r:
            try:
                k = Kill(r)
            except TypeError:
                continue
        if k.VictimInFweddit():
            print("Victim in fweddit")
            logging.info("Victim in fweddit")
            continue
        if k.attackerInFweddit():
            print("Sending message to {0}".format(k.victim['character_id']))
            logging.info("Sending message to {0}".format(k.victim['character_id']))
            ESIMailer.ESIMail(k.victim['character_id'])
            

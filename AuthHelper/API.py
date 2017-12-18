'''
Created on Dec 16, 2017

@author: Brent
'''
import eveapi
import mailbox
import calendar
import re
from email.utils import formatdate, parsedate
from email.mime.text import MIMEText
class EveMail:
    ''' Main class handling message extraction and maildir storage '''
    def __init__( self, charInfo, mailDir = 'eveMail' ):
        self.api      = eveapi.EVEAPIConnection()
        self.auth     = self.api.auth( keyID = charInfo[0], vCode = charInfo[1] )
        self.char     = self.getCharacter( charInfo[2] )
        #self.inbox    = mailbox.Maildir( mailDir )
        self.mail   = self.char
        self.mailList = []

    def __del__( self ):
        try:
            self.inbox.close()
        except AttributeError:
            pass

    def getCharacter( self, name ):
        ''' Gets character object for this account by name '''
        charList = self.auth.account.Characters()
        for character in charList.characters:
            print(character.name.lower())
            if character.name == name:
                name = character.name
                return character
            else:
                print ("%12s: Error - Not found on account" % name)
                exit(2)

    def lastMessageTime( self ):
        ''' Returns date of the last message in mailbox '''
        lastMsgTime = 0
        if len( self.inbox ) > 0:
            lastMsgTime = calendar.timegm(
                    parsedate(
                        sorted(
                            self.inbox.itervalues(),
                            key=lambda item: ( parsedate( item['Date'] ), item )
                        )[-1]['Date']
                    ) )
        return lastMsgTime

    def getMailHeaders( self ):
        ''' Imports new mailheaders from api '''
        mailList = self.auth.char.MailMessages( characterID = self.char.characterID )

        gotTill = self.lastMessageTime()

        for message in mailList.messages:
            if message.sentDate > gotTill:
                self.mailList.append( Message( message ) )

    def getMailBodies( self ):
        ''' Imports mailbodies '''
        idsString = ','.join( str( message.msgId ) for message in self.mailList )
        if len( idsString ) < 1:
            return
        mailList = self.auth.char.MailBodies(
                characterID = self.char.characterID,
                ids = idsString )
        bodyHash = {}
        for message in mailList.messages:
            bodyHash[message.messageID] = message.data

        for message in self.mailList:
            message.body = bodyHash[ message.msgId ]

    def getMailList( self ):
        ''' Loads full messages from api into self.mailList '''
        self.getMailHeaders()
        self.getMailBodies()

    def dumpMail( self ):
        ''' Stores messages in mailbox '''
        for message in self.mailList:
            self.inbox.add( message.mail() )


class Message:
    ''' Message class '''
    def __init__( self, headers, body = '' ):
        self.api       = eveapi.EVEAPIConnection()
        self.msgId     = headers.messageID
        self.sender    = self.idToName( headers.senderID )
        self.recepient = self.idToName( ','.join( [
            str( headers.toCorpOrAllianceID ),
            str( headers.toCharacterIDs ) ] ) )
        self.date      = headers.sentDate
        self.subj      = headers.title
        self.body      = body

    def mail( self ):
        ''' Returns mailobject wich can be added to maildir '''
        mail = MIMEText( self.body.encode( 'utf-8' ), 'html', 'utf-8' )
        mail['Subject'] = self.subj.encode( 'utf-8' )
        mail['Date'] = formatdate( self.date )
        mail['From'] = self.sender.encode( 'utf-8' )
        mail['To'] = self.recepient.encode( 'utf-8' )
        return mail

    def idToName( self, idString ):
        ''' Gets names by ids '''
        if len( str( idString ) ) == 0:
            return ''
        idString = re.sub( ',$', '', str( idString ) )
        charList = self.api.eve.CharacterName( ids = idString )

        nameList = []
        for character in charList.characters:
            #nameList.append( re.sub( "\s+", '_', character.name ) )
            nameList.append( '"' + character.name + '"' )
            #nameList.append( character.name + ' <fake@eveonline.com>' )
        return ','.join( nameList )

if __name__ == '__main__':
    CharInfo = [ 6548270,         # your account-id here
            "T83umHNynNZkA8RNfzy3etfYMdDw8HCaWNAGVLqKazG6eSMqffdibKEKo50yECIG", # limited apikey wont work
            "Lumpy McLumpFace" ]        # which character's mail to read

    try:
        Watcher = EveMail( CharInfo, '/var/spool/mail/something/maildir' ) # path to maildir of your choice
        Watcher.getMailList()
        Watcher.dumpMail()
    except eveapi.Error as exc:
        print ('Failed to fetch new mail: %s' % ( exc ))

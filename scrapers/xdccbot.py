#!/usr/bin/python2
"""
XDCC file downloader

Hacked together by Gregory Eric Sanderson Turcot Temlett MacDonnell Forbes
Requires the python package "twisted"

This script connects to an IRC server and batch downloads files using the XDCC
protocol.

TODO:
 * Manage partial downloads
 * Manage unexpected DCC connections
 * Add optional port to command line

License:

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import sys
import logging as log

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log as twistedlog

class XdccBot( irc.IRCClient ):

    @property
    def nickname( self ):
        return self.factory.nickname

    def connectionMade( self ):
        irc.IRCClient.connectionMade( self )
        log.info("Bot connection made")

    def signedOn( self ):
        log.info("Bot has signed on")
        self.join( self.factory.channel )

    def joined( self, channel ):
        log.info("Bot has joined channel %s" % channel )
        self.processXdccRequests()

    def processXdccRequests( self ):

        xdccmsg = "XDCC SEND #%s"

        if len( self.factory.xdccRequests ) > 0:
            number = self.factory.xdccRequests.pop(0)
            self.msg( self.factory.xdccBot, xdccmsg % str(number) )
        else:
            reactor.stop()

    def privmsg( self, user, channel, msg ):
        log.info( "<%s> %s" % (user, msg) )

    def dccDoSend( self, user, address, port, filename, size, data ):

        factory = XdccDownloaderFactory(
                self,
                filename,
                self.factory.destdir,
                (user, self.factory.channel, data) )

        if not hasattr( self, 'dcc_sessions' ):
            self.dcc_sessions = []
        self.dcc_sessions.append( factory )

        reactor.connectTCP(address, port, factory)

    def dccDownloadFinished( self, filename, success ):

        log.info("Download of %s finished. Download status: %s" %
                ( filename, success ) )
        self.processXdccRequests()

class XdccBotFactory( protocol.ClientFactory ):

    def __init__( self, channel, nickname, xdccBot, xdccRequests, destdir = '.' ):
        self.channel = channel
        self.nickname = nickname
        self.destdir = destdir
        self.xdccBot = xdccBot
        self.xdccRequests = xdccRequests

    def clientConnectionLost(self, connector, reason):
        log.warning("Lost connection. Will try to reconnect. reason : %s" %
                reason)
        connector.connect()

    def buildProtocol( self, addr ):
        bot = XdccBot()
        bot.factory = self
        return bot

    def clientConnectionFailed(self, connector, reason):
        log.warning("Connection failed. reason: %s" % reason)
        reactor.stop()

class XdccDownloader( irc.DccFileReceive ):

    notifyBlockSize = 1024 * 1024

    def __init__( self, filename, filesize=-1, queryData=None, destDir='.',
            resumeOffset=0):

        irc.DccFileReceive.__init__( self, filename, filesize, queryData, destDir,
                resumeOffset )
        self.bytesNotify = 0

    def isDownloadSuccessful( self ):
        return self.bytesReceived == self.fileSize

    def dataReceived( self, data ):
        irc.DccFileReceive.dataReceived( self, data )
        if self.bytesReceived >= self.bytesNotify + self.notifyBlockSize:

            self.bytesNotify += self.notifyBlockSize

            log.info("%s is now at %s bytes" % (self.filename,
                self.bytesReceived) )

    def connectionLost( self, reason ):

        self.fileSize = self.file.tell()
        irc.DccFileReceive.connectionLost( self, reason )

        if hasattr( self.factory.client, 'dccDownloadFinished' ):
            self.factory.client.dccDownloadFinished( self.filename,
                    self.isDownloadSuccessful() )

class XdccDownloaderFactory( protocol.ClientFactory ):

    def __init__( self, client, filename, destdir, queryData ):
        self.client = client
        self.queryData = queryData
        self.filename = filename
        self.destdir = destdir

    def buildProtocol( self, addr ):
        downloader = XdccDownloader(
                self.filename,
                -1,
                self.queryData,
                self.destdir)
        downloader.factory = self
        return downloader

    def clientConnectionFailed( self, connector, reason ):
        log.warning("connection failed during DCC download. reason: %s" %
                reason)
        self.client.dcc_sessions.remove(self)

    def clientConnectionLost( self, connector, reason ):
        self.client.dcc_sessions.remove(self)

if __name__ == "__main__":

    if( len( sys.argv ) < 6 ):
        print "Usage: %s IRC_SERVER CHANNEL NICKNAME BOTNICKNAME XDCC_REQUESTS"
        sys.exit(1)

    log.basicConfig( level = log.INFO )

    observer = twistedlog.PythonLoggingObserver()
    observer.start()

    server, channel, nickname, xdccbot = sys.argv[1:5]
    xdccrequests = sys.argv[5:]

    print server, channel, nickname, xdccbot, xdccrequests

    factory = XdccBotFactory( channel, nickname, xdccbot, xdccrequests )
    reactor.connectTCP( server, 6667, factory )
    reactor.run()

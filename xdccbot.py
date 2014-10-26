import os
import struct
import sys
import random
import irc.client
import irc.logging

def download(connection, user, pack):
    connection.notice(user, "xdcc send #" + str(pack))

class XDCCBot(irc.client.SimpleIRCClient):

    def __init__(self, xdccfile, download_path):
        irc.client.SimpleIRCClient.__init__(self)
        self.download_path = download_path
        self.xdccfile = xdccfile
        self.received_bytes = 0
        self.ctcp_version = "py_ctcp"
        

    def on_nicknameinuse(self, connection, event):
        connection.nick(connection.get_nickname() + "_")

    def on_welcome(self, connection, event):
        connection.join(self.xdccfile.channel)
        print ("joined %s" % (self.xdccfile.channel))

        connection.execute_delayed(random.uniform(2,8), download, (connection, self.xdccfile.user, self.xdccfile.number))

    def on_dccmsg(self, connection, event):
        data = event.arguments[0]
        self.file.write(data)
        self.received_bytes = self.received_bytes + len(data)
        self.dcc.send_bytes(struct.pack("!I", self.received_bytes))

    def on_dccchat(self, connection, event):
        pass

    def on_ctcp(self, connection, event):
        nick = event.source.nick
        
        # CTCP ANSWER TO : VERSION
        if event.arguments[0] == "VERSION":
            connection.ctcp_reply(nick, "VERSION " + self.ctcp_version)
            
        # CTCP ANSWER TO : PING
        elif event.arguments[0] == "PING":
            if len(event.arguments) > 1:
                connection.ctcp_reply(nick, "PING " + event.arguments[1])
                
        # CTCP ANSWER TO : SEND
        elif len(event.arguments) >= 2:       
            args = event.arguments[1].split()
            if args[0] == "SEND":
                self.filename = self.download_path + os.path.basename(args[1])
                if os.path.exists(self.filename):
                    print("A file named", self.filename,)
                    print("already exists. Attempting to resume it.")
                    
                    self.peeraddress = irc.client.ip_numstr_to_quad(args[2])
                    self.position = os.path.getsize(self.filename)
                    
                    cmd = "DCC RESUME #"+ str(self.numPaquet) +" "+ str(args[3]) +" "+ str(self.position)
                    connection.ctcp_reply(self.xdccfile.user, cmd)
                    
                else:
                    self.file = open(self.filename, "wb")
                    peeraddress = irc.client.ip_numstr_to_quad(args[2])
                    peerport = int(args[3])
                    self.dcc = self.dcc_connect(peeraddress, peerport, "raw")
                    
            elif args[0] == "ACCEPT" :
                print("on_ctcp RESUME")
                self.file = open(self.filename, "ab")
                peerport = int(args[2])
                self.dcc = self.dcc_connect(self.peeraddress, peerport, "raw")
                
            else:
                self.connection.quit()

    def on_dcc_disconnect(self, connection, event):
        self.file.close()
        print("Received file %s (%d bytes)." % (self.filename,
                                                self.received_bytes))
        self.connection.quit()

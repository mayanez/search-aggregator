import json
import Queue
import hexchat
import time

__module_name__ = "xdccmanager"
__module_version__ = "0.0.0.1"
__module_description__ = "Python module for managing XDCC"

class XDCCFile(object):
    def __init__(self, name, network, channel, user, number, size):
        self.__name = name
        self.__network = network
        self.__channel = channel
        self.__user = user
        self.__number = number
        self.__size = size

    def __str__(self):
        return self.__name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def network(self):
        return self.__network

    @network.setter
    def network(self, value):
        self.__network = value


    @property
    def channel(self):
        return self.__channel

    @channel.setter
    def channel(self, value):
        self.__channel = value

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, value):
        self.__user = value

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, value):
        self.__number = value

class XDCCManager(object):
    def __init__(self, download_dir):
        self.xdcc_file_queue = None
        self.server = ""

    def loadFile(self, file_name):
        self.xdcc_file_queue = Queue.Queue()
        a_file = open(file_name)
        json_data = json.load(a_file)
        self.server = json_data["network"]
        for obj in json_data["files"]:
            self.xdcc_file_queue.put(XDCCFile(obj["name"], json_data["network"], obj["channel"], obj["user"], obj["number"], obj["size"]))

    def connectServer(self):
        if (hexchat.get_info("server") != self.server):
            hexchat.command("server %s" % (self.server))

    def joinChannel(self, channel):
        if (hexchat.get_info("channel") != channel):
            hexchat.command("join #%s" % (channel))

    def getChannels(self):
        unique_channels = set()
        for xdcc_file in self.xdcc_file_queue:
            unique_channels.add(xdcc_file.channel)
        return unique_channels

    def getFiles(self):
        if not self.xdcc_file_queue.empty():
            xdcc_file = self.xdcc_file_queue.get()
            hexchat.prnt("Getting " + xdcc_file.name)
            self.joinChannel(xdcc_file.channel)
            #Double check in correct channel by /whois on bot
            hexchat.command("msg %s xdcc send #%s" % (xdcc_file.user, xdcc_file.number))
            return True
        return False

    def getFiles_callback(self, word, word_eol, userdata):
        self.getFiles()
        return hexchat.EAT_ALL

    def setup(self, word, word_eol, userdata):
        argc = len(word)
 
        if argc == 2:
            if word[1] == "start":
                hexchat.hook_print("DCC RECV Complete", self.getFiles_callback)
                self.getFiles()
            elif word[1] == "stop":
                hexchat.hook_unload(self.getFiles_callback)
            elif word[1] == "load":
                self.loadFile(word[2])
            elif word[1] == "queue":
                hexchat.prnt(str(self.xdcc_file_queue))
        
        return hexchat.EAT_ALL   

if __name__ == '__main__':
    hexchat.prnt("XDCC Manager Loaded")
    #Move these values to Config json
    xdccManager = XDCCManager("/Volumes/DeathStar/Torrents")
    xdccManager.loadFile("/Users/mayanez/.config/hexchat/addons/downloadlist.json")
    
    hexchat.hook_command("XDCC", xdccManager.setup, help="/XDCC <cmd>")





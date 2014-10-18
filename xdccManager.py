import json
import Queue
import XDCCFile
import irc.client

class XDCCManager(object):
	def __init__(self):
		self.client = DCCReceive()
		self.xdcc_file_list = list()
		self.file_queue = Queue.Queue()
		self.download_dir = "."

	def loadFile(self, file_name):
		json_data = open(file_name)
		for item in json_data:
			self.xdcc_file_list.append(json.load(item, object_hook=self.__XDCCFile_decoder))

	def addToQueue(self, file):
		self.file_queue.put(file)

	def __XDCCFile_decoder(obj):
		return XDCCFile(obj["name"], obj["network"], obj["channel"], obj["user"], obj["number"], obj["size"])
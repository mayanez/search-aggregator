class XDCCFile(object):
	def __init__(self, name, network, channel, user, number, size, requests):
		self.__name = name
		self.__network = network
		self.__channel = channel
		self.__user	= user
		self.__number = number
		self.__size = size
		self.__requests = requests

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

	@property
	def size(self):
		return self.__size

	@size.setter
	def size(self, value):
		self.__size = value

	@property
	def requests(self):
		return self.__requests

	@requests.setter
	def requests(self, value):
		self.__requests = value



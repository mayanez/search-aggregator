import requests
import urllib
import XDCCFile
from bs4 import BeautifulSoup

class haruhichanScraper(object):
	def __init__(self):
		self.url = "http://intel.haruhichan.com"
		
		self.params = {
			"s" : ""
		}

	def search(self, query):
		self.params["s"] = query
		
		response = requests.get(self.url, params=self.params)
		soup = BeautifulSoup(response.text)

		xdcc_file_list = list()

		results_table = soup.find("table", {"id": "packListTable"})
		result_body = results_table.find("tbody")
		file_list = result_body.findAll("tr")

		for a_file in file_list:
			file_info = a_file.findAll("td")
			user = file_info[0].get_text()
			number = file_info[1].get_text()
			num_requested = file_info[2].get_text()
			size = file_info[3].get_text()
			name = file_info[4].get_text()
			network = "irc.rizon.net"
			channel = "#intel"
			xdcc_file = XDCCFile.XDCCFile(name, network, channel, user, number, size, num_requested)
			xdcc_file_list.append(xdcc_file)

		return xdcc_file_list


if __name__ == '__main__':
	scraper = haruhichanScraper()
	results = scraper.search("E7DACD61")
	print results[0]





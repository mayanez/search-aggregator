import requests
import urllib
import XDCCFile
from bs4 import BeautifulSoup
from urlparse import urlparse

class ixircScraper(object):
	def __init__(self):
		self.url = "http://ixirc.com"
		
		self.params = {
			"q" : "",
			"pn" : "0"
		}

	def search(self, query, pages=2):
		self.params["q"] = query
		results = list()

		max_pages = self.__maxPages(query)

		for page in xrange(pages):
			if (page <= max_pages):
				results += self.__search(query, page)
			else:
				break

		return results

	def __search(self, query, page):
		self.params["q"] = query
		self.params["pn"] = page
		response = requests.get(self.url, params=self.params)
		soup = BeautifulSoup(response.text)

		xdcc_file_list = list()

		results_table = soup.find("table", {"id": "results-table"})

		file_list = results_table.findAll("tr", {"class" : ["even", "odd"]})

		for a_file in file_list:
			file_info = a_file.findAll("td")
			name = file_info[0].get_text()
			parsed_network = urlparse(file_info[0].find("a", {"class": "result-dl"})["href"])
			network = "{uri.hostname}".format(uri=parsed_network)
			channel = file_info[2].get_text().replace('#', '')
			user = file_info[3].get_text()
			number = file_info[4].get_text()
			gets = file_info[5].get_text()
			size = file_info[6].get_text()
			xdcc_file = XDCCFile.XDCCFile(name, network, channel, user, number, size, gets)
			xdcc_file_list.append(xdcc_file)

		return xdcc_file_list

	def __maxPages(self, query):

		self.params["q"] = query
		self.params["pn"] = 0
		response = requests.get(self.url, params=self.params)
		soup = BeautifulSoup(response.text)

		page_numbers = soup.find("div", {"class" : "page-numbers"})
		max_pages = page_numbers.findAll("a")[-1].get_text()
		
		return int(max_pages)

if __name__ == '__main__':
	scraper = ixircScraper()
	results = scraper.search("hi")
	print results[0]


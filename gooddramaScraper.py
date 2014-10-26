import requests
import urllib
import XDCCFile
from bs4 import BeautifulSoup
from urlparse import urlparse
from collections import namedtuple

Series = namedtuple("Series", "name url")

class GoodDramaScraper(object):
	def __init__(self):
		self.url = "http://www.gooddrama.net/drama/search"
		
		self.params = {
			"key" : "",
			"stype" : "drama"
		}


	def search(self, query):
		self.params["key"] = query
		response = requests.get(self.url, params=self.params)
		soup = BeautifulSoup(response.text)

		search_results = list()

		results = soup.find("div", {"id" : "content"})
		series_list = results.findAll("div", {"class" : "series_list"})
		series = series_list[0].findAll("div", {"class" : "right_col"})
		
		for s in series:
			info = s.find("h3").find("a")
			
			search_results.append(Series(info.get_text(), info["href"]))

		return search_results

if __name__ == '__main__':
	scraper = GoodDramaScraper()

	scraper.search("line")
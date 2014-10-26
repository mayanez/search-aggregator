import requests
import urllib
import re
from bs4 import BeautifulSoup
from urlparse import urlparse
from collections import namedtuple

Series = namedtuple("Series", "name url")

class AnimeSeasonScraper(object):
	def __init__(self):
		self.url = "http://animeseason.com/anime-list"
		
		self.params = {
			"search" : ""
		}


	def search(self, query):
		self.params["search"] = query
		response = requests.get(self.url, params=self.params)
		soup = BeautifulSoup(response.text)
		search_results = list()

		anime_series = soup.find("div", {"class" : "content_bloc"}).findAll("li")

		for s in anime_series:
			title = s.get_text()
			url = "http://animeseason.com" + s.find("a")["href"]
			if (query.lower() in title.lower()):
				search_results.append(Series(title, url))

		return search_results
if __name__ == '__main__':
	scraper = AnimeSeasonScraper()

	print scraper.search("sword art")
import requests
import urllib
from KickassAPI import Torrent
from bs4 import BeautifulSoup
from urlparse import urlparse

class DAddictsScraper(object):
	def __init__(self):
		self.url = "http://www.d-addicts.com/forum/torrents.php"
		
		self.params = {
			"search" : ""
		}


	def search(self, query):
		self.params["search"] = query
		response = requests.get(self.url, params=self.params)
		soup = BeautifulSoup(response.text)
		
		search_results = list()

		results = soup.findAll("a", {"class" : "topictitle"})
		for drama in results:
				
			name = drama.get_text() # Title
			download_link = drama["href"] # Forum link
			drama_info = drama.parent.parent.findAll("td")
			magnet_link = drama_info[3].find("a")["href"] #Magnet link
			category = drama_info[0].get_text() # Category
			size = drama_info[5].get_text()
			age = drama_info[7].get_text()
			search_results.append(Torrent(name, "", "", category, size, "", age, "", "", "", "", "", magnet_link, download_link))

		return search_results


if __name__ == '__main__':
	scraper = DAddictsScraper()

	print scraper.search("mozu")
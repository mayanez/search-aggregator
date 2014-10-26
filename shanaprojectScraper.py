import requests
import urllib
from KickassAPI import Torrent
from bs4 import BeautifulSoup
from urlparse import urlparse

class ShanaProjectScraper(object):
	def __init__(self):
		self.url = "http://www.shanaproject.com/search/"
		
		self.params = {
			"title" : "",
			"subber" : ""
		}

	#Only searches first page. Don't think its necessary to search more for now.
	def search(self, query):
		self.params["title"] = query
		response = requests.get(self.url, params=self.params)
		soup = BeautifulSoup(response.text)

		search_results = list()

		anime_titles = soup.findAll("div", {"class": "release_title"})

		for anime in anime_titles:
			series = anime.find("a").get_text()
			shana_series_url = "http://www.shanaproject.com" + anime.find("a")["href"]
			episode = anime.parent.find("div", {"class" : "release_episode"}).get_text()
			
			quality = anime.parent.find("div", {"class" : ["release_quality_hd", "release_quality_sd"]})
			if (quality is not None):
				quality = quality.get_text()
			
			subber = anime.parent.find("div", {"class" : "release_subber"}).find("a").get_text().replace("\n", "")
			profile_list = anime.parent.findAll("span", {"class" : "release_profile"})
			profiles = ""
			for p in profile_list:
				profiles += p.get_text() + " "

			size = anime.parent.find("div", {"class" : "release_size"}).get_text()
			
			url = anime.find("div", {"class" : "release_info"})
			if (url is not None):
				url = url.find("a")["href"]
			
			torrent_link = anime.parent.find("div", {"class" : "release_download"})
			if (torrent_link is not None):
				torrent_link = "http://www.shanaproject.com" + torrent_link.parent["href"]

			title = "[%s] %s - %s %s %s" % (subber, series, episode, quality, profiles)
			search_results.append(Torrent(title, subber, "", "Anime", size, "", "", "", "", "", "", torrent_link, "", shana_series_url))

		return search_results

if __name__ == '__main__':
	scraper = ShanaProjectScraper()
	scraper.search("sword art online")
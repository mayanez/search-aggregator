Search Aggregator
============

* Searchs various sites across the net. Aggregates all results in one useful location.
* Includes Standalone XDCC Downloader.
* Integrates with Transmission for torrent links.
* Easy extensible. Feel free to add your own search providers to be aggregated.

  To start webapp run `python scraperManager.py`.
  
Please note this is still a work in progress. Basic functionality is there, but needs a lot more work. I would like to get the UI up to par once I finish flushing out the backend.

DEPENDENCIES
============
There are quite a few. I need to compile a full list and add it to a setup.py file. The main one for scrapers is BeautifulSoup & Requests.

TODO
====
Still a work in progress. Need to flush out Transmission integration + UI. Also, refactor scraperManager to be more modular.

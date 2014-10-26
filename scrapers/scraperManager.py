import haruhichanScraper
import ixircScraper
import daddictsScraper
import gooddramaScraper
import animeseasonScraper
import shanaprojectScraper
import os
import xdccbot
import KickassAPI
import urllib2
import logging as log
from multiprocessing import Process
from flask import Flask, render_template, send_from_directory, request, redirect
from twisted.internet import reactor, protocol
from twisted.python import log as twistedlog
from crunchyroll.apis.meta import MetaApi
from tpb import TPB
from transmission import Transmission

app = Flask(__name__)


app.config.update(
    DEBUG = True,
)

#Initiaze various search engines
haruhichan_scraper = haruhichanScraper.haruhichanScraper()
ixirc_scraper = ixircScraper.ixircScraper()
daddicts_scraper = daddictsScraper.DAddictsScraper()
shanaproject_scraper = shanaprojectScraper.ShanaProjectScraper()
crunchyroll = MetaApi()
gooddrama_scraper = gooddramaScraper.GoodDramaScraper()
animeseason_scraper = animeseasonScraper.AnimeSeasonScraper()
tpb = TPB('https://thepiratebay.org')
transmission_client = Transmission(host='torrentserver', port=9091, username='transmission', password='transmission')

#----------------------------------------
# controllers
#----------------------------------------

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/search", methods=['GET'])
def search():
    query = request.args.get('q')

    #Call search engines
    
    #XDCC
    haruhichan_xdcc_file_list = haruhichan_scraper.search(query)
    ixirc_xdcc_file_list = ixirc_scraper.search(query)
    xdcc_file_list = haruhichan_xdcc_file_list + ixirc_xdcc_file_list

    #Streaming Sites
    crunchyroll_series = crunchyroll.search_anime_series(query)
    gooddrama_series = gooddrama_scraper.search(query)
    animeseason_series = animeseason_scraper.search(query)

    #Torrents
    #TODO: Unify results into one Torrent object
    kickass_torrents = KickassAPI.Search(query)
    tpb_torrents = tpb.search(query)
    daddicts_torrents = daddicts_scraper.search(query)
    shanaproject_torrents = shanaproject_scraper.search(query)
    

    return render_template('search.html', xdcc=xdcc_file_list, crunchyroll=crunchyroll_series, 
        gooddrama=gooddrama_series, animeseason=animeseason_series, torrents=kickass_torrents, 
        tpb_torrents=tpb_torrents, daddicts_torrents=daddicts_torrents, shanaproject_torrents=shanaproject_torrents)

@app.route("/hexchat", methods=['GET'])
def hexchat():
    channel = str(request.args.get('channel'))
    user = str(request.args.get('user'))
    pack = str(request.args.get('pack'))

    #Call hexchat using my XDCCManager
    return "hexchat"

@app.route("/deluge")
def deluge():
    #Add torrent to deluge
    return "deluge"

@app.route("/transmission")
def transmission():
    file_name=urllib2.unquote(str(request.args.get('url'))).decode()
    #TryCatch
    transmission_client('torrent-add', filename=file_name)
    return redirect("http://torrentserver:9091/")
#----------------------------------------
# launch
#----------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8888))
    app.run(host='0.0.0.0', port=port)
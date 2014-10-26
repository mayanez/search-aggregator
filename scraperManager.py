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
import threading
import ConfigParser
import logging as log
from multiprocessing import Process
from flask import Flask, render_template, send_from_directory, request, redirect
from twisted.internet import reactor, protocol
from twisted.python import log as twistedlog
from crunchyroll.apis.meta import MetaApi
from tpb import TPB
from transmission import Transmission
from XDCCFile import XDCCFile

app = Flask(__name__)

app.config.update(
    DEBUG = True,
)

Config = ConfigParser.ConfigParser()
if Config.read('settings.cfg') == []:
    print "Please copy the settings.cfg.example to settings.cfg"
    raise Exception('Could not read config file')

webapp_port = Config.get("webapp", "port")
downloadPath = Config.get("xdcc", "downloadpath")
xdccNick = Config.get("xdcc", "nick")
transmission_rpc_host = Config.get("transmission", "rpc-host")
transmission_rpc_port = int(Config.get("transmission", "rpc-port"))
transmission_redirect_url = Config.get("transmission", "redirect-url")
transmission_rpc_username = Config.get("transmission", "username")
transmission_rpc_password = Config.get("transmission", "password")

#Initiaze various search engines
haruhichan_scraper = haruhichanScraper.haruhichanScraper()
ixirc_scraper = ixircScraper.ixircScraper()
daddicts_scraper = daddictsScraper.DAddictsScraper()
shanaproject_scraper = shanaprojectScraper.ShanaProjectScraper()
crunchyroll = MetaApi()
gooddrama_scraper = gooddramaScraper.GoodDramaScraper()
animeseason_scraper = animeseasonScraper.AnimeSeasonScraper()
tpb = TPB('https://thepiratebay.org')
transmission_client = Transmission(host=transmission_rpc_host, port=transmission_rpc_port, username=transmission_rpc_username, password=transmission_rpc_password)

xdccPool = []
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
    try:
        kickass_torrents = KickassAPI.Search(query)
    except:
        kickass_torrents = list()
    tpb_torrents = tpb.search(query)
    daddicts_torrents = daddicts_scraper.search(query)
    shanaproject_torrents = shanaproject_scraper.search(query)
    

    return render_template('search.html', xdcc=xdcc_file_list, crunchyroll=crunchyroll_series, 
        gooddrama=gooddrama_series, animeseason=animeseason_series, torrents=kickass_torrents, 
        tpb_torrents=tpb_torrents, daddicts_torrents=daddicts_torrents, shanaproject_torrents=shanaproject_torrents)

@app.route("/xdcc", methods=['GET'])
def xdcc():
    server = str(request.args.get('server'))
    channel = "#" + str(request.args.get('channel'))
    user = str(request.args.get('user'))
    pack = str(request.args.get('pack'))
    
    p = Process(target=do_xdcc, args=(server, channel, user, pack))
    p.start()
    p.join()
    return "Check the shared drive for your file."

@app.route("/deluge")
def deluge():
    #Add torrent to deluge
    return "deluge"

@app.route("/transmission")
def transmission():
    file_name=urllib2.unquote(str(request.args.get('url'))).decode()
    #TryCatch
    transmission_client('torrent-add', filename=file_name)
    return redirect(transmission_redirect_url)

#----------------------------------------
# launch
#----------------------------------------
def do_xdcc(server, channel, user, pack):
    xdccfile = XDCCFile("", server, channel, user, pack, "", "")
    bot = xdccbot.XDCCBot(xdccfile, downloadPath)
    bot.connect(server, 6667, xdccNick)
    bot.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", webapp_port))
    app.run(host='0.0.0.0', port=port)
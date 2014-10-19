import haruhichanScraper
import ixircScraper
import os
import xdccbot
import logging as log
from multiprocessing import Process
from flask import Flask, render_template, send_from_directory, request
from twisted.internet import reactor, protocol
from twisted.python import log as twistedlog


app = Flask(__name__)


app.config.update(
    DEBUG = True,
)
#----------------------------------------
# controllers
#----------------------------------------

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/search", methods=['GET'])
def search():
    query = request.args.get('q')
    haruhichan_scraper = haruhichanScraper.haruhichanScraper()
    ixirc_scraper = ixircScraper.ixircScraper()

    haruhichan_xdcc_file_list = haruhichan_scraper.search(query)
    ixirc_xdcc_file_list = ixirc_scraper.search(query)

    xdcc_file_list = haruhichan_xdcc_file_list + ixirc_xdcc_file_list
    return render_template('search.html', result=xdcc_file_list)

@app.route("/download", methods=['GET'])
def download():
    file_name = str(request.args.get('name'))
    server = str(request.args.get('server'))
    channel = str(request.args.get('channel'))
    user = str(request.args.get('user'))
    pack = str(request.args.get('pack'))
    log.basicConfig( level = log.INFO )

    #Do better interprocess communication. To minimize openning and closing of IRCBot
    p = Process(target=do_xdcc, args=(server, channel, user, pack))
    p.start()
    p.join()

    return send_from_directory(".", file_name)

#----------------------------------------
# launch
#----------------------------------------

def do_xdcc(server, channel, user, pack):
    observer = twistedlog.PythonLoggingObserver()
    observer.start()

    factory = xdccbot.XdccBotFactory( channel, "desuyo", user, [pack] )
    reactor.connectTCP( server, 6667, factory )
    reactor.run()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8888))
    app.run(host='0.0.0.0', port=port)
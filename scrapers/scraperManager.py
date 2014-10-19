import haruhichanScraper
import ixircScraper
import os
from flask import Flask, render_template, send_from_directory, request
from Naked.toolshed.shell import execute_js, muterun_js
from subprocess import call

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
	file_name = request.args.get('name')
	server = request.args.get('server')
	channel = request.args.get('channel')
	user = request.args.get('user')
	pack = request.args.get('pack')
	node_params = "%s %s %s %s" % (server, channel, user, pack)

	success = execute_js("xdcc.js", arguments=node_params)

	if success:
		return send_from_directory(".", file_name)
	return "error"
#----------------------------------------
# launch
#----------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8888))
    app.run(host='0.0.0.0', port=port)
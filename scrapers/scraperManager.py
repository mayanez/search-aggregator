import haruhichanScraper
import os
from flask import Flask, render_template, send_from_directory, request

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
	scraper = haruhichanScraper.haruhichanScraper()
	xdcc_file_list = scraper.search(query)
	return render_template('search.html', result=xdcc_file_list)

#----------------------------------------
# launch
#----------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8888))
    app.run(host='0.0.0.0', port=port)
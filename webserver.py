from flask import Flask
import scrapeweb
app = Flask(__name__)

@app.route("/")
def hello():
    text = scrapeweb.get_article_text('https://www.sciencedaily.com/releases/2019/02/190221141511.htm')
    return text
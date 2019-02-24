from flask import Flask, render_template, jsonify
from flask_cors import CORS, cross_origin
import scrapeweb
app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:5000"}})



@app.route("/data")
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def hello():
    text = scrapeweb.get_article_text(url)
    
    response = jsonify(text)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/')
def home():
    return render_template('hackillinoisHTML.html')

@app.route('/js')
def js():
    return render_template('hackillinoisJS.js')

@app.route('/css')
def css():
    return render_template('hackillinoisCSS.css')


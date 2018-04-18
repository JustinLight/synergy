from flask import Flask, render_template, jsonify
import json
import urllib.request

app=Flask(__name__)




@app.route('/')
def index():
    return render_template('home.html')

@app.route('/background_card')
def getcard():
    return jsonify(json.load(urllib.request.urlopen('https://api.scryfall.com/cards/random'))['image_uris']['small'])



@app.route('/about')
def about():
    return render_template('about.html')

if __name__=='__main__':
    app.run(debug=True)

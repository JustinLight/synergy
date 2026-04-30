from flask import Flask, render_template, jsonify
import scrython

app=Flask(__name__)



@app.route('/')
def index():
    return render_template('home.html')

@app.route('/background_card')
def getcard():
    card = scrython.cards.Random()
    return jsonify(card.image_uris['normal']) 



@app.route('/about')
def about():
    return render_template('about.html')

if __name__=='__main__':
    app.run(debug=True)

from flask import Flask, render_template
from magic import getcard

app=Flask(__name__)




@app.route('/')
def index():
    return render_template('home.html', card = getcard('https://api.scryfall.com/cards/random'),
    card2=getcard('https://api.scryfall.com/cards/random'),
    card3=getcard('https://api.scryfall.com/cards/random'),
    card4=getcard('https://api.scryfall.com/cards/random'),
    card5=getcard('https://api.scryfall.com/cards/random'),
    card6=getcard('https://api.scryfall.com/cards/random'),
    card7=getcard('https://api.scryfall.com/cards/random'),
    card8=getcard('https://api.scryfall.com/cards/random'),
    card9=getcard('https://api.scryfall.com/cards/random'),
    card10=getcard('https://api.scryfall.com/cards/random'))

@app.route('/about')
def about():
    return render_template('about.html')

if __name__=='__main__':
    app.run(debug=True)

import json
import urllib.request




def getcard(cardurl):
    cardurl=cardurl
    image=json.load(urllib.request.urlopen(cardurl))
    card=image['image_uris']['normal']
    return card

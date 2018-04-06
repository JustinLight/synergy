import json
import urllib.request




def getcard(cardurl):
    return json.load(urllib.request.urlopen(cardurl))['image_uris']['normal']

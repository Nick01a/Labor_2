import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl
import requests
import folium
from flask import Flask, render_template, request


def find_location(location):


    google_maps_api = 'https://maps.googleapis.com/maps/api/geocode/json'
    argum = {'address': location, "key": "AIzaSyABvGeZU5brsu-PefU2-SsA7UIDbSThB5k"}


    req = requests.get(google_maps_api, params=argum)
    res = req.json()
    result = res['results']
    try:
        result = (result[0])
    except IndexError:
        return None

    location_of = []
    location_of.append(result['geometry']['location']['lat'])
    location_of.append(result['geometry']['location']['lng'])

    return location_of

def friends(name, option, count):
    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'


    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE


    info = {}
    info_1={}
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': name,'count' : count})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()

    js = json.loads(data)

    for i in js['users']:
        info[i["screen_name"]] = i[option]
    for j in info:
        info_1[j] = find_location(info[j])
    return info_1
#print(friends("tesla","location",10))


def show_map(friend):


    map = folium.Map()
    for i in friend:
        if friend[i]:
            map.add_child(folium.Marker(location=friend[i],
                                                     popup=i,
                                                     icon=folium.Icon(icon='cloud')))
            map.add_child(folium.CircleMarker(location=friend[i],
                                               radius=10,
                                               popup=i,
                                               color="red",
                                               icon=folium.Icon(color='black',icon='info-sign')))
            map.add_child(folium.CircleMarker(location=friend[i],
                                                     radius=5,
                                                     popup=i,
                                                     color="black",
                                                     icon=folium.Icon()))

    map.add_child(folium.LayerControl())
    map.save("/home/Nick0/mysite//Map.html")
    return "Map.html"
#print(show_map(friends("nba","location",10)))

app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        res = request.form['name']
        name_of = friends(res, "location", 10)
        return render_template(show_map(friends(name_of)))


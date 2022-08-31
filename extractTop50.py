import requests, base64
import pandas as pd
import json
import configparser
from datetime import date
from dateutil.parser import parse
from os.path import exists

def getToken(client_id, client_secret):
    auth = '{}:{}'.format(client_id, client_secret)
    b64auth = base64.b64encode(auth.encode()).decode()
    header = {"Authorization": "Basic %s" % b64auth,
              "Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}
    return requests.post("https://accounts.spotify.com/api/token", headers=header, data=data)

def getPlaylist(token):
    auth = "Bearer {}".format(token)
    header = {"Accept":"application/json", "Content-Type": "application/json",
        "Authorization":auth}
    return requests.get("https://api.spotify.com/v1/playlists/37i9dQZEVXbMDoHDwVN2tF", headers=header)

parser = configparser.ConfigParser()
parser.read("billboardify.conf")
client_id = parser.get("spotify_credentials", "client_id")
client_secret = parser.get("spotify_credentials", "client_secret")

token = getToken(client_id, client_secret)
if token.status_code != 200:
    print("Status code:", token.status_code)
    print("Response:", token.json())
    exit()

token = token.json()
token = token['access_token']

response = getPlaylist(token)

raw_data = './data/raw/top50/{}.json'.format(date.today())
with open(raw_data,'w') as f:
    f.write(response.text)

# if something goes wrong, exit with status code
if response.status_code != 200:
    print("Status code:",response.status_code)
    print("Response:", response.json())
    exit()

dic = json.loads(response.text)
items = dic['tracks']['items']
date_added = [parse(item['added_at']).date() for item in items]
# date_added = [date.date() for date in date_added]

track_names = [item['track']['name'] for item in items]

artists = [[artist['name'] for artist in item['track']['artists']] for item in items]
artists = [','.join(artist) for artist in artists]

df = pd.DataFrame({'date_added': date_added, 'track': track_names, 'artist': artists})
file_path = './data/structured/top50Global.csv'
if exists(file_path):
    df.to_csv(file_path, mode='a', header=False, index=False)
else:
    df.to_csv(file_path, index=False)

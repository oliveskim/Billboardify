import requests, base64
import pandas as pd
import json
import configparser

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

# sanity check
# write this to have a look at the responses json
'''with open('response.json','w') as f:
    f.write(response.text)'''

# only execute if the request was successful
if response.status_code == 200:
    dic = json.loads(response.text)
    items = dic['tracks']['items']
    track_names = [item['track']['name'] for item in items]
    artists = [[artist['name'] for artist in item['track']['artists']] for item in items]
    artists = [','.join(artist) for artist in artists]
    df = pd.DataFrame({'track': track_names, 'artist': artists})
    # try small query
    # for artist in df['artist']:
    #     if 'Bad Bunny' in artist:
    #         print(artist)
    df.to_csv("top50Global.csv", index=False)
# if something goes wrong, print the status code
else:
    print(response.status_code)

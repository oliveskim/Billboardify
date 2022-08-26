import requests
import pandas as pd
import json

# this token expires with some requests and an hour or two
token = 'BQAsHLFu3ohdxmj4HNnhiOTbZuH_0jb7XVezyP5K8KV8AANwSTP04xiRUVcXXCPFHrI7t_OZwLGiNY9zwdhrqn1dXbozzmtJs9PAC2Mv5MCB3Gp3WYGm9LDHLSUjKYm5f7xHp0onJUSsSf3l8L2IGqMTmZ9soaOWCY3rKcPpFg'
auth = "Bearer {}".format(token)
header = {"Accept":"application/json", "Content-Type": "application/json",
    "Authorization":auth}
response = requests.get("https://api.spotify.com/v1/playlists/37i9dQZEVXbMDoHDwVN2tF", headers=header)

# sanity check
# write this to have a look at the responses json
'''with open('response.json','w') as f:
    f.write(response.text)'''

if response.status_code == 200:
    dic = json.loads(response.text)
    items = dic['tracks']['items']
    track_names = [item['track']['name'] for item in items]
    artists = [[artist['name'] for artist in item['track']['artists']] for item in items]
    df = pd.DataFrame({'track': track_names, 'artist': artists})
    # try small query
    for artist in df['artist']:
        if 'Bad Bunny' in artist:
            print(artist)
    df.to_csv("top50Global.csv", index=False)
    #print(df)
    # create new df reading from the first file
    df2 = pd.read_csv("top50Global.csv")
    print("")
    # compare new df's output
    for artist in df2['artist']:
        if 'Bad Bunny' in artist:
            print(artist)
else:
    print(response)

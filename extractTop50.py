import requests
import pandas as pd
import json

# this token expires with some requests and an hour or two
token = 'BQCmrfhqNkMyiTLVXeWXQf0XteTmdLtqTiC_p8zD5j1AS9hPxVgdRrlcpd5oqjrDMFKL0PWgY-HX-zmMlVj-nt1UYVrftVXjbmZxHRpDXJ0K1tQis8qqSUCwkhAD0J-piFXpeXTHgDJA-Dp2NwjQqC6XDHoiq1CB2kBUtz3F4w'
auth = "Bearer {}".format(token)
header = {"Accept":"application/json", "Content-Type": "application/json",
    "Authorization":auth}
response = requests.get("https://api.spotify.com/v1/playlists/37i9dQZEVXbMDoHDwVN2tF", headers=header)

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
    print(df.head())
    print(df2.head())
# if something goes wrong, print the status code
else:
    print(response.status_code)

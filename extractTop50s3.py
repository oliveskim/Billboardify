import requests, base64
import pandas as pd
import json
import configparser
from datetime import date
import boto3
from dateutil.parser import parse

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
aws_access = parser.get("amazon_credentials", "aws_access")
aws_secret = parser.get("amazon_credentials", "aws_secret")
bucket='billboardify'

s3 = boto3.client('s3', 
                  region_name='sa-east-1',
                  aws_access_key_id=aws_access,
                  aws_secret_access_key=aws_secret)

token = getToken(client_id, client_secret)
if token.status_code != 200:
    print("Status code:", token.status_code)
    print("Response:", token.json())
    exit()

token = token.json()
token = token['access_token']

response = getPlaylist(token)

response_key = 'data/raw/top50/{}.json'.format(date.today())

#uploading response to s3 bucket
s3.put_object(
    Body=response.text.encode(),
    Bucket=bucket,
    Key=response_key)

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

#if key does not exist, upload normally, if it does, get the object and append it locally
#get the existing csv

file_path = 'data/structured/top50Global.csv'
todays_top50 = df.to_csv(None, header=None, index=False).encode()

try:
    current_top50 = s3.get_object(Bucket=bucket, Key=file_path)
except:
    s3.put_object(Body=todays_top50,
                  Bucket=bucket,
                  Key=file_path)
else:
    updated_top50 = current_top50 + todays_top50
    s3.put_object(Body=updated_top50,
                  Bucket=bucket,
                  Key=file_path)


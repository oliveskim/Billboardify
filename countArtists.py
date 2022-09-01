import pandas as pd
import boto3
import configparser 

bucket='billboardify'

parser = configparser.ConfigParser()
parser.read("billboardify.conf")
aws_access = parser.get("amazon_credentials", "aws_access")
aws_secret = parser.get("amazon_credentials", "aws_secret")


s3 = boto3.client('s3', 
                  region_name='sa-east-1',
                  aws_access_key_id= aws_access,
                  aws_secret_access_key=aws_secret)


def countGlobal(artist):
    count = 0
    for art in top50['artist']:
        if artist in art:
            count += 1
    return count

billboard_path = './data/structured/distinct_artists_billboard_10s.csv'

with open(billboard_path) as f:
    artists = f.readlines()
    hot100 = [line.rstrip() for line in artists]

top50_path = './data/structured/top50Global.csv'
top50 = pd.read_csv(top50_path)

artist_count = [countGlobal(artist) for artist in hot100]
result = pd.DataFrame({"artist":hot100, "count":artist_count})
result_path = './data/structured/artists_count.csv'
result.to_csv(result_path, index=False)
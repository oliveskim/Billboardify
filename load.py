from distutils.command.config import config
import boto3 
import awswrangler as wr
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

s3.upload_file(
    Filename='./data/raw/billboard_10s_cru.csv',
    Bucket=bucket,
    Key='data/raw/billboard_10s_cru.csv')

s3.upload_file(
    Filename='./data/structured/billboard_10s.csv',
    Bucket=bucket,
    Key='data/structured/billboard_10s.csv')

s3.upload_file(
    Filename='./data/structured/distinct_artists_billboard_10s.csv',
    Bucket=bucket,
    Key='data/structured/distinct_artists_billboard_10s.csv')
#todas as partes para a extração e pré tratamento dos dados, salvando em um arquivo csv
import billboard
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

def tuple_to_df(chart, size=100):
    """
    Creates a pandas DataFrame from a billboard.ChartData object.

    Args: 
        chart: billboard ChartData object
        size (optional): number of rows in the chart object
            default: 100 rows

    """
    chart_name, chart_entries = (chart.title, [{'Title': i.title, 'Artists': i.artist, 'Rank': i.rank} for i in chart.entries])
    df = pd.DataFrame(chart_entries, dtype='string', index=range(1, size+1))
    df['Chart Name'] = chart_name
    return df

chart_name = 'decade-end/hot-100'

chart_10s = billboard.ChartData(chart_name)

df_chart_10s = tuple_to_df(chart_10s)

key_arquivo_cru = 'data/raw/billboard_10s_cru.csv'
chart_10s_csv = df_chart_10s.to_csv(None, header=None, index=False).encode()
s3.put_object(
              Body=chart_10s_csv,
              Bucket=bucket,
              Key=key_arquivo_cru)

#Transformation part: Separating artists in a list

df_chart_replaced = df_chart_10s

artists_list = []
for i in df_chart_replaced['Artists']:   
    artists_list.append(i.replace(' & ',', ').replace(' Featuring ',', ').replace(' + ', ', ').replace('Pharrell', 'Pharrell Williams').replace('Williams Williams','Williams'))

df_chart_replaced['Artists'] = artists_list

key_arquivo = 'data/structured/billboard_10s.csv'

chart_replaced_csv = df_chart_replaced.to_csv(None, header=None, index=False).encode()
s3.put_object(
              Body=chart_replaced_csv,
              Bucket=bucket,
              Key=key_arquivo)
              
#Transformations part: distinct artists

distinct_artists_list = []

for i in df_chart_replaced['Artists']:
    j = i.split(', ')
    for n in range(len(j)):
        if j[n] not in distinct_artists_list:
            distinct_artists_list.append(j[n])

distinct_artists_df = pd.DataFrame(distinct_artists_list, columns= ['Artists'], index=range(1, 101))

key_arquivo_distintos = 'data/structured/distinct_artists_billboard_10s.csv'

chart_distintos_csv = distinct_artists_df.to_csv(None, header=None, index=False).encode()
s3.put_object(
              Body=chart_distintos_csv,
              Bucket=bucket,
              Key=key_arquivo_distintos)
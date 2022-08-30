#todas as partes para a extração e pré tratamento dos dados, salvando em um arquivo csv
from datetime import datetime
import billboard
import pandas as pd

def string_to_date(x):
    return datetime.strptime(x, '%Y-%m-%d')

def tuple_to_df(chart, size=100):
    """
    Creates a pandas DataFrame from a billboard.ChartData object.

    Args: 
        chart: billboard ChartData object
        size (optional): number of rows in the chart object

    """
    chart_name, chart_entries = (chart.title, [{'Title': i.title, 'Artist': i.artist, 'Rank': i.rank} for i in chart.entries])
    df = pd.DataFrame(chart_entries, dtype='string', index=range(1, size+1))
    df['Chart Name'] = chart_name
    return df

chart_name = 'decade-end/hot-100'

chart_10s = billboard.ChartData(chart_name)

print(type(chart_10s))

df_chart_10s = tuple_to_df(chart_10s)

print(df_chart_10s.head(10))

path_arquivo = './data/raw/billboard_10s_cru.csv'

with open(path_arquivo, 'w'):
    df_chart_10s.to_csv(path_arquivo, index=False)

df_chart_replaced = df_chart_10s

test = []
for i in df_chart_replaced['Artist']:   
    test.append(i.replace(' & ',', ').replace(' Featuring ',', '))

df_chart_replaced['Artist'] = test

print(df_chart_10s.head(10))

path_arquivo2 = './data/structured/billboard_10s.csv'

with open(path_arquivo2, 'w'):
    df_chart_replaced.to_csv(path_arquivo2, index=False)
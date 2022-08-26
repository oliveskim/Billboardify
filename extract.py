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
    chart_name, chart_entries = (chart.title, [{'Title': i.title, 'Artist': i.artist, 'Featuring Artist': i.artist, 'Rank': i.rank} for i in chart.entries])
    df = pd.DataFrame(chart_entries, dtype='string', index=range(1, size+1))
    df['Chart Name'] = chart_name
    return df

def separate_column_in_df(df, column='Artist', column2='Featuring Artist', sep=" Featuring "):
    """
    Separate a column in a dataframe using a given string as a separator.
    
    Args:
        df: pandas DataFrame to be manipulated
        column: column to be separated, if no column is given,
        defaults to 'Artist'
        column2: column that will recieve the second part of the separated string,
        defaults to 'Featuring Artist'
        sep: separator to be used, default is " Featuring "
    """
    df_temp1 = df
    df_temp2 = df
    df_temp2[column] = df[column].str.split(sep, n=1).str.get(0)
    df_temp2[column2] = df_temp1[column2].str.split(sep, n=1).str.get(1)

    return df_temp2


chart_name = 'decade-end/hot-100'

chart_10s = billboard.ChartData(chart_name)

print(type(chart_10s))

df_chart_10s = tuple_to_df(chart_10s)

print(df_chart_10s.head(10))


df_chart_10s_new = separate_column_in_df(df_chart_10s)

print(df_chart_10s_new.head(10))

path_arquivo = './arquivos/billboard_10s.csv'

with open(path_arquivo, 'w'):
    df_chart_10s_new.to_csv(path_arquivo, index=False)

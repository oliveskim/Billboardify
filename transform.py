import pandas as pd
import pandasql as ps


path_arquivo = './data/structured/billboard_10s.csv'

with open(path_arquivo, 'r'):
    df = pd.read_csv(path_arquivo)

#distinct_artists_df = pd.DataFrame(columns='Artist')

df2 = df['Artists'].split(', ')

q1 = """SELECT DISTINCT(Artists) FROM df"""

distinct_artists_df = ps.sqldf(q1, locals())

print(distinct_artists_df.head(5))
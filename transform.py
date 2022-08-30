import pandas as pd
import pandasql as ps


path_arquivo = './data/structured/billboard_10s.csv'

df = pd.read_csv(path_arquivo)

distinct_artists_list = []

for i in df['Artists']:
    for n in range(len(i.split(', '))):
        if i.split(', ')[n] not in distinct_artists_list:
            distinct_artists_list.append(i.split(', ')[n])

df2 = pd.DataFrame(distinct_artists_list, columns= ['Artists'], index=range(1, 101))

q1 = """SELECT DISTINCT(Artists) FROM df2"""

distinct_artists_df = ps.sqldf(q1, locals())

path_arquivo = './data/structured/distinct_artists_billboard_10s.csv'

with open(path_arquivo, 'w'):
    distinct_artists_df.to_csv(path_arquivo, index=False)
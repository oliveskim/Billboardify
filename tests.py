import pandas as pd
import pandasql as ps

df_top50 = pd.read_csv('./top50Global.csv')

q1 = """SELECT COUNT(*) FROM df_top50
        WHERE date_added = '2022-08-29 10:48:58+00:00'"""
q2 = """SELECT COUNT(*) FROM df_top50
        WHERE date_added = '2022-08-30 10:42:30+00:00'"""

count_dia_29 = ps.sqldf(q1, locals())
count_dia_30 = ps.sqldf(q2, locals())

print(count_dia_29)
print(count_dia_30)

df_distinct = pd.read_csv('./data/structured/distinct_artists_billboard_10s.csv')

q3 = """SELECT COUNT(Artists) FROM df_distinct"""
q4 = """SELECT COUNT(DISTINCT(Artists)) FROM df_distinct"""

count_artists_df = ps.sqldf(q3, locals())
count_distinct_artists_df = ps.sqldf(q4, locals())

#'O arquivo de artistas distintos só possui artistas distintos? '

print(count_artists_df)
print(count_distinct_artists_df)
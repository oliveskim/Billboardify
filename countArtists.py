import pandas as pd

def countGlobal(artist):
    count = 0
    for art in top50['artist']:
        if artist in art:
            count += 1
    return count

with open("billboard_10s.csv") as f:
    artists = f.readlines()
    hot100 = [line.rstrip() for line in artists]

top50 = pd.read_csv("top50Global.csv")

artist_count = [countGlobal(artist) for artist in hot100]
result = pd.DataFrame({"artist":hot100, "count":artist_count})
result.to_csv("result.csv", index=False)
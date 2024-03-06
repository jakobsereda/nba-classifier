from nba_api.stats.endpoints import playercareerstats, commonallplayers
import pandas as pd
import json
import time

players = commonallplayers.CommonAllPlayers()

players_frame = players.get_data_frames()[0]
ids = players_frame['PERSON_ID']
n = len(ids)
print(n, ids[0], ids[n-1])
i = 0

results = []
errors = []

def get_player_career(id: int):
    global i, result
    print(f"Fetching {i}/{n} - {id}.....       ", end="\r")
    i += 1
    time.sleep(0.5)
    try:
        vals = playercareerstats.PlayerCareerStats(player_id=id).get_dict()
        d = {}
        for result in vals['resultSets']:
            if result['name'] == "SeasonTotalsRegularSeason":
                for (idx, header) in enumerate(result['headers']):
                    rows = result['rowSet']
                    if len(rows) > 0:
                        d[header] = rows[-1][idx]
                break
        results.append(d)
    except:
        errors.append(id)
    return id

stats = ids[:].map(get_player_career)
# print(results)
df = pd.DataFrame(results)
df.to_csv("stats.csv")
with open("errors.json", "w") as f:
    f.write(json.dumps(errors))
    f.close()

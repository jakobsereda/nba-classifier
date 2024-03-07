from nba_api.stats.endpoints import commonplayerinfo, playercareerstats, commonallplayers
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


def parse_results(info, career):
    d = {}
    for vals in [info, career]:
        for result in vals['resultSets']:
            for (idx, header) in enumerate(result['headers']):
                rows = result['rowSet']
                if len(rows) > 0:
                    d[header] = rows[-1][idx]
            break
    return d

def get_player_career(id: int):
    global i, result
    print(f"Fetching {i}/{n} - {id}.....       ", end="\r")
    i += 1
    time.sleep(0.5)
    try:
        career = playercareerstats.PlayerCareerStats(player_id=id).get_dict()
        info = commonplayerinfo.CommonPlayerInfo(player_id=id).get_dict()
        results.append(parse_results(info, career))
    except:
        errors.append(id)
    return id

stats = ids[:50].map(get_player_career)
df = pd.DataFrame(results)
df.to_csv("stats.csv")
with open("errors.json", "w") as f:
    f.write(json.dumps(errors))
    f.close()

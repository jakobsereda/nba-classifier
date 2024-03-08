from nba_api.stats.endpoints import commonplayerinfo, playercareerstats, commonallplayers
import pandas as pd
import time
import json

players = commonallplayers.CommonAllPlayers()

players_frame = players.get_data_frames()[0]
ids = players_frame['PERSON_ID']
n = len(ids)
i = 0

results = []
errors = []

def fetch(path: str, count: int = -1):
    if count == -1:
        count = len(ids)
    start_time = time.time()

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
        curr_time = time.time()
        elapsed = curr_time - start_time
        remaining = int(elapsed / i * (count - i)) if i > 0 else 0
        print(f"[{'=' * int(50 * i / count)}{' ' * int(50 * (1 - (i / count)))}] {i}/{count}: {id} | Elapsed: {int(elapsed) // 60}m{int(elapsed) % 60}s | Remaining: ~{remaining // 60}m{remaining % 60}s        ", end="\r")
        # print(f"Fetching {i}/{count} - {id}.....       \n[{'=' * int(50 * i / count)}{' ' * int(50 * (1 - (i / count)))}]", end="\r")
        i += 1
        time.sleep(0.5)
        try:
            career = playercareerstats.PlayerCareerStats(player_id=id).get_dict()
            info = commonplayerinfo.CommonPlayerInfo(player_id=id).get_dict()
            results.append(parse_results(info, career))
        except:
            errors.append(id)
        return id

    ids[:count].map(get_player_career)
    df = pd.DataFrame(results)
    df.to_csv(path, index=False)
    with open("errors.json", "w") as f:
        f.write(json.dumps(errors))
        f.close()

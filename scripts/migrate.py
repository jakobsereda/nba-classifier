import pandas as pd
import numpy as np
import math

def height_to_in(height) -> int:
    # height format from api is FT-IN (e.g. 6-10 for 6'10")
    if not isinstance(height, str):
        return height
    ft, inch = map(int, height.split("-"))
    return ft * 12 + inch

def int_remove_nan(num):
    if not isinstance(num, float):
        return num
    elif math.isnan(num):
        return pd.NA
    return int(num)

def flag_to_bool(flag) -> bool:
    # endpoint returns some fields as Y/N
    if not isinstance(flag, str):
        return flag
    return flag.upper() == "Y"

def migrate(path: str):
    df = pd.read_csv(path)
    migrations = {
        "HEIGHT": [ height_to_in, int_remove_nan ],
        "WEIGHT": [ int_remove_nan ],
        "PLAYER_ID": [ int_remove_nan ],
        "PLAYER_AGE": [ int_remove_nan ],
        "JERSEY": [ int_remove_nan ],
        "GAMES_PLAYED_CURRENT_SEASON_FLAG": [ flag_to_bool ],
        "DLEAGUE_FLAG": [ flag_to_bool ],
        "NBA_FLAG": [ flag_to_bool ],
        "GAMES_PLAYED_FLAG": [ flag_to_bool ],
        "GREATEST_75_FLAG": [ flag_to_bool ],
        "GP": [ int_remove_nan ],
        "LEAGUE_ID": [ int_remove_nan ],
        "GS": [ int_remove_nan ],
        "MIN": [ int_remove_nan ],
        "FGM": [ int_remove_nan ],
        "FGA": [ int_remove_nan ],
        "FG3M": [ int_remove_nan ],
        "FG3A": [ int_remove_nan ],
        "FTM": [ int_remove_nan ],
        "FTA": [ int_remove_nan ],
        "OREB": [ int_remove_nan ],
        "DREB": [ int_remove_nan ],
        "REB": [ int_remove_nan ],
        "AST": [ int_remove_nan ],
        "STL": [ int_remove_nan ],
        "BLK": [ int_remove_nan ],
        "TOV": [ int_remove_nan ],
        "PF": [ int_remove_nan ],
        "PTS": [ int_remove_nan ]
    }
    for (col, funcs) in migrations.items():
        for (i, func) in enumerate(funcs):
            print(f"Running migration {i+1} for column {col}...       ")
            df[col] = df[col].apply(func)
    df.to_csv(path, index=False)

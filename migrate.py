import pandas as pd
import numpy as np
import math

def height_to_in(height) -> int:
    # height format from api is FT-IN (e.g. 6-10 for 6'10")
    if not isinstance(height, str):
        return height
    ft, inch = map(int, height.split("-"))
    return ft * 12 + inch

def jersey_to_int(jersey):
    if not isinstance(jersey, float):
        return jersey
    elif math.isnan(jersey):
        return pd.NA
    return int(jersey)

def flag_to_bool(flag) -> bool:
    # endpoint returns some fields as Y/N
    if not isinstance(flag, str):
        return flag
    return flag.upper() == "Y"

def migrate(path: str):
    df = pd.read_csv(path)
    migrations = {
        "HEIGHT": height_to_in,
        "PLAYER_AGE": int,
        "JERSEY": jersey_to_int,
        "GAMES_PLAYED_CURRENT_SEASON_FLAG": flag_to_bool,
        "DLEAGUE_FLAG": flag_to_bool,
        "NBA_FLAG": flag_to_bool,
        "GAMES_PLAYED_FLAG": flag_to_bool,
        "GREATEST_75_FLAG": flag_to_bool
    }
    for (col, func) in migrations.items():
        print(f"Running migration for column {col}...       ", end = "\r")
        df[col] = df[col].apply(func)
    df.to_csv(path, index=False)

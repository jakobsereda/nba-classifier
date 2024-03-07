import pandas as pd

def height_to_in(height) -> int:
    if not isinstance(height, str):
        return height
    # height format from api is FT-IN (e.g. 6-10 for 6'10")
    ft, inch = map(int, height.split("-"))
    return ft * 12 + inch

def migrate(path: str):
    df = pd.read_csv(path)
    migrations = {
        "HEIGHT": height_to_in,
        "PLAYER_AGE": int
    }
    for (col, func) in migrations.items():
        df[col] = df[col].apply(func)
    df.to_csv(path)

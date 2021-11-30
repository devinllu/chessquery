import requests
from chessdotcom import get_player_games_by_month_pgn, get_player_games_by_month
from pprint import pprint
import pandas as pd

def get_stats(username):
    res = requests.get(f"https://api.chess.com/pub/player/{username}/stats")
    return res.json()

def get_games(username, year, month):
    """
    Return List[Dict[str, Any]] of games
    """
    res = get_player_games_by_month(username, year, month)
    return res.json['games']

def main():
    # res = ccom.get_player_profile('lusthetics')
    # res = res.json
    # print(res['player']['followers'])

    obj = get_games("lusthetics", "2019", "03")
    first_game = obj

    df = pd.DataFrame(first_game)

    print(df.iloc[0].keys())

    # print(obj)

if __name__ == "__main__":
    main()
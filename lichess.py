import berserk
import pandas as pd

API_TOKEN = "lip_bYPixWzHsRrAjtPMeUwP"

def getLichessToken():
    return API_TOKEN

def getLichessDataByPlayerAsJSON(client, username, max, color):
    return client.games.export_by_player(username=username, as_pgn=False, rated=True, opening=True, max=max, color=color)

def saveLichessDataByPlayerToCSV(client, username, max, color):
    lst = list(client.games.export_by_player(username=username, as_pgn=False, rated=True, opening=True, max=max, color=color))
    
    df = pd.DataFrame(lst)
    df.to_csv(f"{username}.csv", index=False)

def main():
    pass

if __name__ == "__main__":
    main()
import berserk
import pandas as pd

API_TOKEN = "lip_bYPixWzHsRrAjtPMeUwP"

def getLichessToken():
    return API_TOKEN

def getLichessDataByPlayerAsJSON(client, username, max):
    return client.games.export_by_player(username=username, as_pgn=False, rated=True, opening=True, max=max)


def main():
    pass

if __name__ == "__main__":
    main()
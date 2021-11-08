import lichess as li
import pandas as pd
import berserk
import json
from pprint import pprint

def main():
    LICHESS_API_TOKEN = li.getLichessToken()
    session = berserk.TokenSession(LICHESS_API_TOKEN)
    client = berserk.Client(session=session)

    lusthetics = li.getLichessDataByPlayerAsJSON(client, "Lusthetics", 10)
    lusthetics = list(lusthetics)
    # df = pd.read_json(lusthetics)

    pprint(lusthetics[0])

if __name__ == "__main__":
    main()
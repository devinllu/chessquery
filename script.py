import lichess as li


import berserk

def main():
    LICHESS_API_TOKEN = li.getLichessToken()
    session = berserk.TokenSession(LICHESS_API_TOKEN)
    client = berserk.Client(session=session)


    li.saveLichessDataByPlayerToCSV(client=client, username="Lusthetics", max=1000, color=berserk.Color.WHITE)

if __name__ == "__main__":
    main()
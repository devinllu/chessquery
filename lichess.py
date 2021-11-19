import berserk
import pandas as pd

# token expires in 30 days
API_TOKEN = "lip_bYPixWzHsRrAjtPMeUwP"

session = berserk.TokenSession(API_TOKEN)
client = berserk.Client(session=session)

def get_token():
    return API_TOKEN

def get_color(color):
    if color.lower() == 'white':
        return berserk.Color.WHITE

    return berserk.Color.BLACK

def save_by_player(username, max, color):
    
    lst = list(client.games.export_by_player(username=username, as_pgn=False, rated=True, opening=True, max=max, color=get_color(color)))
    
    df = pd.DataFrame(lst)
    filename = username.lower()
    df.to_csv(f"data/{filename}.csv", index=False)

def main():
    pass

if __name__ == "__main__":
    main()
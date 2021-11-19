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

def get_variant(variant):
    if variant.lower() == 'bullet':
        return berserk.PerfType.BULLET
    if variant.lower() == 'blitz':
        return berserk.PerfType.BLITZ
    if variant.lower() == 'rapid':
        return berserk.PerfType.RAPID

def save_by_player(username, max, color, variant):
    
    lst = list(client.games.export_by_player(username=username, as_pgn=False, rated=True, opening=True, max=max, perf_type=get_variant(variant), color=get_color(color)))
    
    df = pd.DataFrame(lst)
    filename = username.lower()
    df.to_csv(f"data/{filename}.csv", index=False)

def main():
    pass

if __name__ == "__main__":
    main()
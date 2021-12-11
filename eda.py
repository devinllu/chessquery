import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress


def show_winrate(file_src):
    data = pd.read_csv(file_src, low_memory=False)

    data = data.drop(['site', 'utctime', 'moves_played', 'opening'], axis=1)
    data = data.dropna()

    games = len(data)

    white_wins = len(data[data.result == '1-0'])
    black_wins = len(data[data.result == '0-1'])
    draw = len(data[data.result == '1/2-1/2'])

    print("white wins: " + str(white_wins))
    print("black_wins: " + str(black_wins))
    print("draw: " + str(draw))

    print("winrate of white: " + str(white_wins / (white_wins + black_wins)))
    print("winrate of black: " + str(black_wins / (white_wins + black_wins)))

    print("winrate of white excluding draws: " + str(white_wins / games))
    print("winrate of black excluding draws: " + str(black_wins / games))
    print("draw rate: " + str(draw / games))


def show_distribution(file_src):
    data = pd.read_csv(file_src, low_memory=False)

    data = data.drop(['site', 'utctime', 'moves_played', 'opening'], axis=1)
    data = data.dropna()

    data['whiteelo'] = (data['whiteelo'].astype(float) / 10).astype(int) * 10
    data['blackelo'] = (data['blackelo'].astype(float) / 10).astype(int) * 10

    ratings = pd.DataFrame({'sum': [],
                            'elos': []})

    mean1 = data['whiteelo'].sum() / len(data)
    mean2 = data['blackelo'].sum() / len(data)

    mean = round((mean1 + mean2) / 2, 2)

    print(mean)

    temp = data['whiteelo']
    temp = temp.append(data['blackelo'])

    ratings['elos'] = temp
    ratings['sum'] = 1

    ratings = ratings.groupby(['elos']).sum()

    plt.figure(figsize=(10, 5))

    plt.plot(ratings)
    plt.xlabel("Rating")
    plt.ylabel("Players")
    plt.axvline(mean, color='green', linestyle='dashed', linewidth=3)
    plt.legend(['mean: ' + str(mean)])

    plt.show()


def show_castle_distribution(file_src):
    data = pd.read_csv(file_src, low_memory=False)

    data = data.drop(['site', 'utctime', 'moves_played', 'opening'], axis=1)
    data = data.dropna()

    data['result'].loc[(data['result'] == '0-1')] = 0
    data['result'].loc[(data['result'] == '1-0')] = 1
    data['result'].loc[(data['result'] == '1/2-1/2')] = 0.5

    data['rating_average'] = (data['rating_average'].astype(float) / 50).astype(int) * 50

    black_castled = data[data.castled == 2]
    white_castled = data[data.castled == 1]

    b_ratings = pd.DataFrame({'result': [],
                            'rating_average': []})
    w_ratings = pd.DataFrame({'result': [],
                            'rating_average': []})

    b_ratings['result'] = black_castled['result']
    b_ratings['rating_average'] = black_castled['rating_average']

    w_ratings['result'] = white_castled['result']
    w_ratings['rating_average'] = white_castled['rating_average']

    b_ratings = b_ratings.groupby(['rating_average']).mean()
    w_ratings = w_ratings.groupby(['rating_average']).mean()

    b_ratings = b_ratings[:-1]
    w_ratings = w_ratings[:-1]

    print(b_ratings)
    print("line here")
    print(w_ratings)

    w_line = 0.5166
    b_line = 1 - w_line

    plt.figure(figsize=(10, 5))

    plt.plot(b_ratings)
    plt.axhline(b_line, color='green', linestyle='-')
    plt.xlabel("Rating")
    plt.ylabel("Winrate(including draws)")
    plt.title("Winrate of Black when Castling")

    plt.show()

    plt.figure(figsize=(10, 5))

    plt.plot(w_ratings)
    plt.axhline(w_line, color='green', linestyle='-')
    plt.xlabel("Rating")
    plt.ylabel("Winrate (including draws)")
    plt.title("Winrate of White when Castling")

    plt.show()


def show_f3_distribution(file_src):
    data = pd.read_csv(file_src, low_memory=False)

    data = data.drop(['site', 'utctime', 'moves_played', 'opening'], axis=1)
    data = data.dropna()

    played_f3 = data[data.played_f3 == 0]

    played_f3['result'].loc[(data['result'] == '0-1')] = 0
    played_f3['result'].loc[(data['result'] == '1-0')] = 1
    played_f3['result'].loc[(data['result'] == '1/2-1/2')] = 0.5

    white_wins = len(played_f3[played_f3.result == '1-0'])
    black_wins = len(played_f3[played_f3.result == '0-1'])
    draw = len(played_f3[played_f3.result == '1/2-1/2'])

    played_f3['rating_average'] = (played_f3['rating_average'].astype(float) / 50).astype(int) * 50

    print(played_f3)

    ratings = pd.DataFrame({'result': [],
                            'rating_average': []})

    ratings['result'] = played_f3['result']
    ratings['rating_average'] = played_f3['rating_average']

    ratings = ratings.groupby(['rating_average']).mean()

    ratings = ratings[:-4]

    print(ratings)

    plt.figure(figsize=(10, 5))

    line = 0.5166

    plt.plot(ratings)
    plt.axhline(line, color='green', linestyle='-')
    plt.xlabel("Rating")
    plt.ylabel("Winrate (including draws)")
    plt.title("Winrate of White when playing f3")

    plt.show()


def main():
    # measure_attributes("data/lichess-std-big.csv")
    # show_distribution("C:\data\lichess_db_standard_rated_2021-10.csv")

    file_src = "./data/lichess_db_standard_rated_2021-10-subset.csv"

    # show_distribution("./data/smalldata.csv")

    # plots below:

    show_winrate(file_src)
    show_distribution(file_src)
    show_f3_distribution(file_src)
    show_castle_distribution(file_src)


if __name__ == "__main__":
    main()

import csv
import sys

import pandas as pd

# takes in string parameter and returns a shorter code
def classify_event(event):
    # match event:
    #     case "Rated Bullet game":
    #         return 1
    #     case "Rated Blitz game":
    #         return 2
    #     case "Rated Rapid game":
    #         return 3
    #     case "Rated Classical game":
    #         return 4
    #     case _:
    #         exit("Found ")
    if event == 'Rated Bullet game':
        return 1
    elif event == 'Rated Blitz game':
        return 2
    elif event == 'Rated Rapid game':
        return 3
    elif event == 'Rated Classical game':
        return 4
    else:
        exit("Did not find matching event")


def get_substring_in_quotes(input_str):
    i = 0
    while input_str[i] != '"':
        i += 1

    i += 1
    substr = ''

    while input_str[i] != '"':
        substr = substr + input_str[i]
        i += 1

    return substr


def parse_pgn(file_src, file_output, show_event=True, show_site=False, show_date=True, show_names=False, elo=True, show_rating_diff=True,
         show_opening_code=True, show_opening_name=False, show_tc=True, show_termination=True, show_moves=False):
    file_src = './data/lichess_db_standard_rated_2013-01.txt'
    file_output = './data/lichess_db_standard_rated_2013-01.csv'

    file = open(file_src)
    file = list(enumerate(file))

    i = 0           #line number

    data = []      #2d array of games

    try:
        while True:                     #loop for each games
            arr = []                    #array of game info

            # loop for each row for info
            # once out of loop, the next line is moves played. The line after that is
            # a newline, before the [Event ""] of the next game.
            while file[i][1] != '\n':
                info = get_substring_in_quotes(file[i][1])
                arr.append(info)
                i += 1

            i += 1

            if show_moves:
                # todo: haven't done moves yet
                pass

            i += 2

            data.append(arr)

    except IndexError:
        pass

    df = pd.DataFrame(data)
    df.to_csv(file_output,index=False,header=False)

def main():
    file_src = './data/lichess_db_standard_rated_2013-01.txt'
    file_output = './data/lichess_db_standard_rated_2013-01.csv'
    parse_pgn(file_src=file_src,file_output=file_output)


if __name__ == "__main__":
    main()

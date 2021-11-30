import csv
import sys

import pandas as pd
import numpy as np


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
    elif event == 'Rated Correspondence game':
        return 5
    elif event.find('tournament'):
        return 6
    else:
        print(event)
        exit("Did not find matching event")


def classify_termination(termination):
    if termination == 'Normal':
        return 1
    elif termination == 'Time forfeit':
        return 2
    else:
        print(termination)
        exit("Did not find matching termination")


class substr:
    title: ''
    param: ''


def get_substring(input_str):
    data = substr

    title = ''
    param = ''

    i = 1
    while input_str[i] != ' ':
        title = title + input_str[i]
        i += 1

    i += 2

    while input_str[i] != '"':
        param = param + input_str[i]
        i += 1

    data.title = title.lower()
    data.param = param

    return data


def get_moves(input_str):
    data = substr

    # i = 0
    # while input_str[i] != '\n': #not useful right now
    #     param = param + input_str[i]
    #     i += 1

    data.title = 'moves'
    data.param = input_str

    return data


# returns a new column based on the moves played.
def add_column(condition, input_str):
    if condition == 'played_f3':
        index_of = input_str.find('. f3')  # white played f3
        if index_of == -1:
            return 0
        else:
            return 1
    elif condition == 'castled':
        white_castled = input_str.count('. O-O')
        total_castled = input_str.count(' O-O')

        if total_castled == 0:
            return 0
        elif white_castled == 0:  # total_castled = 1
            return 2
        elif total_castled == 2:
            return 3
        else:  # white_castled == 1 and total_castled == 1:
            return 1


def parse_pgn(file_src, file_output, show_event=True, show_site=False, show_player_names=True, show_result=True,
              show_date=True, show_time=False, show_names=False, show_elo=True, show_rating_diff=True,
              show_opening_code=True, show_opening_name=False, show_tc=True, show_termination=True, show_f3_played=True,
              show_castled=True, show_moves=False):
    # note, show moves

    file = open(file_src)
    file = list(enumerate(file))

    col_names = [['event', 'site', 'white', 'black', 'result', 'utcdate', 'utctime', 'whiteelo',
                  'blackelo', 'whiteratingdiff', 'blackratingdiff', 'eco', 'opening',
                  'timecontrol', 'termination', 'moves_played']]

    i = 0  # line number

    data = []  # 2d array of games
    played_f3 = np.array(['played_f3'])
    castled = np.array(['castled'])

    try:
        while True:  # loop for each games
            arr = []  # array of game info

            # loop for each row for info
            # once out of loop, the next line is moves played. The line after that is
            # a newline, before the [Event ""] of the next game.
            while file[i][1] != '\n':
                info = get_substring(file[i][1])

                i += 1

                if info.title == 'event':
                    if not show_event:
                        info.param = ''
                    info.param = classify_event(info.param)
                elif info.title == 'site':
                    if not show_site:
                        info.param = ''
                elif info.title == 'white' or info.title == 'black':
                    if not show_player_names:
                        info.param = ''
                elif info.title == 'result':
                    if not show_result:
                        info.param = ''
                elif info.title == 'utcdate':
                    if not show_date:
                        info.param = ''
                elif info.title == 'utctime':
                    if not show_time:
                        info.param = ''
                elif info.title == 'whiteelo' or info.title == 'blackelo':
                    if not show_elo:
                        info.param = ''
                elif info.title == 'whiteratingdiff' or info.title == 'blackratingdiff':
                    if not show_rating_diff:
                        info.param = ''
                elif info.title == 'eco':
                    if not show_opening_code:
                        info.param = ''
                elif info.title == 'opening':
                    if not show_opening_name:
                        info.param = ''
                elif info.title == 'timecontrol':
                    if not show_tc:
                        info.param = ''
                elif info.title == 'termination':
                    if not show_termination:
                        info.param = ''
                    info.param = classify_termination(info.param)
                elif info.title == 'blacktitle' or info.title == 'whitetitle':
                    continue
                else:
                    print("shouldn't have gotten here!")
                    print(info.title)

                arr.append(info.param)

            i += 1

            info = get_moves(file[i][1])

            if show_moves:
                arr.append(info.param)
            if show_f3_played:
                played_f3 = np.append(played_f3, add_column('played_f3', info.param))
            if show_castled:
                castled = np.append(castled, add_column('castled', info.param))

            i += 2

            data.append(arr)

    except IndexError:
        pass

    df = pd.DataFrame()

    df = df.append(col_names)
    df = df.append(data)

    df['played_f3'] = played_f3.tolist()
    df['castled'] = castled.tolist()

    df.to_csv(file_output, index=False, header=False)


def main():
    # file_src = './data/lichess_db_standard_rated_2013-01.pgn'
    # file_output = './data/lichess_db_standard_rated_2013-01.csv'

    file_src = './data/smallsubset.pgn'
    file_output = './data/smallsubset.csv'

    parse_pgn(file_src=file_src, file_output=file_output)


if __name__ == "__main__":
    main()
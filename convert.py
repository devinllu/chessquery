import csv
import linecache
import sys
import time

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
    elif termination == 'Abandoned':
        return 3
    elif termination == 'Unterminated': #Happens in correspondence games - One side times out
        return 4
    elif termination == 'Rules infraction': #Happens when a cheater is detected while they are playing.
        return 5
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

    if input_str[0] != '[': #games could end in 0 moves
        data = get_moves(input_str)
        return data

    i = 1

    while input_str[i] != ' ':
        title = title + input_str[i]
        i += 1

    i += 2

    try:
        while input_str[i] != '"':
            param = param + input_str[i]
            i += 1
    except IndexError:
        print(input_str)
        print("seems to have a problem...")



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
def add_column(condition, input_str, pgn_format):
    input_str = str(input_str)
    if pgn_format == "old":
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
            elif white_castled == 0:  # total_castled == 1
                return 2
            elif total_castled == 2:
                return 3
            else:  # white_castled == 1 and total_castled == 1:
                return 1
    elif pgn_format == "new":
        if condition == 'played_f3':
            both_played = input_str.count('. f3 ')  # white played f3
            white_played = both_played - input_str.count('... f3 ')
            if white_played == 1:
                return 0
            else:
                return 1
        elif condition == 'castled':
            black_castled = input_str.count('... O-O ')
            total_castled = input_str.count('. O-O ')

            if total_castled == 0:
                return 0
            elif black_castled == 0:  # total_castled == 1, white castled
                return 1
            elif total_castled == 2:
                return 3
            else:  # black_castled == 1 and total_castled == 1:
                return 2


def parse_pgn(file_src, file_output, show_event=True, show_site=False, show_player_names=True, show_result=True,
              show_date=True, show_time=False, show_names=False, show_elo=True, show_rating_diff=True,
              show_opening_code=True, show_opening_name=False, show_tc=True, show_termination=True, show_f3_played=True,
              show_castled=True, show_moves=False, suppress_extra_columns=True):
    # note, show moves

    #pgn_format = input("type in 'new' or 'old' for moveset format: ")
    pgn_format = 'new'
    print('pgn_format currently set to new!')

    col_names = [['event', 'site', 'white', 'black', 'result', 'utcdate', 'utctime', 'whiteelo',
                  'blackelo', 'whiteratingdiff', 'blackratingdiff', 'eco', 'opening',
                  'timecontrol', 'termination', 'moves_played', 'rating_difference', 'rating_average']]

    if show_f3_played:
        col_names[0].append('played_f3')

    if show_castled:
        col_names[0].append('castled')

    i = 0  # line number
    acc = 0
    skip = False

    data = [[]]  # 2d array of games
    played_f3 = []
    castled = []

    start_time = time.perf_counter()
    runtime = 0

    df = pd.DataFrame()

    df = df.append(col_names)
    df.to_csv(file_output, index=False, header=False, mode='a')

    del df

    #line = linecache.getline(file_src, 333333)line_number = 34

    line_number = 34

    with open(file_src) as infile:
        arr = []  # array of game info
        flag = False
        for line in infile:

            # temp += 1
            # if line != '[Site "https://lichess.org/mik2AxQr"]' or checkpoint:
            #     if temp % 1000000 == 0:
            #         end_time = time.perf_counter()
            #         runtime = end_time - start_time
            #
            #         print("Line: " + str(temp) + " " + "runtime: " + str(runtime) + " seconds.")
            #     continue

            # loop for each row for info
            # once out of loop, the next line is moves played. The line after that is
            # a newline, before the [Event ""] of the next game.
            
            if line[0] == '\n':
                continue

            info = get_substring(line)

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
                if info.param == '?':
                    skip = True
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
            elif info.title == 'moves':
                if show_f3_played:
                    played_f3.append(add_column('played_f3', info.param, pgn_format))
                if show_castled:
                    castled.append(add_column('castled', info.param, pgn_format))
                if not show_moves:
                    info.param = ''
            else:
                if not suppress_extra_columns:
                    print("shouldn't have gotten here!")
                    print("error: title key is: " + info.title)
                continue

            arr.append(info.param)

            if skip:
                skip = False
                continue

            if info.title == 'moves':
                data.append(arr)
                acc += 1
                arr = []
                flag = True

            if acc % 500000 == 0 and acc != 0 and flag:
                print("completed game " + str(acc) + ". Doing intermediate processing")

                df = pd.DataFrame()
                df = df.append(col_names)
                df = df.append(data)

                df.columns = df.iloc[0]
                df = df.iloc[1:, :]
                df = df[df['whiteelo'].notna()]

                df['rating_difference'] = abs(df['whiteelo'].astype(int) - df['blackelo'].astype(int))
                df['rating_average'] = (df['whiteelo'].astype(float) + df['blackelo'].astype(float)) / 2
                df['played_f3'] = played_f3
                df['castled'] = castled

                df.to_csv(file_output, index=False, header=False, mode='a')

                end_time = time.perf_counter()
                runtime = end_time - start_time

                print("runtime: " + str(runtime) + " seconds.")

                # resetting parameters

                arr = []
                data = []
                played_f3 = []
                castled = []

                flag = False

                if acc == 5000000:
                    break

            # if acc % 300 == 0 and acc != 0:
            #     break


    print("now starting post processing")
    print("total games: " + str(acc))

    df = pd.DataFrame()
    df = df.append(col_names)
    df = df.append(data)

    df.columns = df.iloc[0]
    df = df.iloc[1:, :]
    df = df[df['result'].notna()]

    df['rating_difference'] = abs(df['whiteelo'].astype(int) - df['blackelo'].astype(int))
    df['rating_average'] = (df['whiteelo'].astype(float) + df['blackelo'].astype(float)) / 2
    df['played_f3'] = played_f3
    df['castled'] = castled

    df.to_csv(file_output, index=False, header=False, mode='a')

    end_time = time.perf_counter()
    runtime = end_time - start_time

    print("Finished. Runtime: " + str(runtime))


def main():
    #file_src = './data/lichess_db_standard_rated_2013-01.pgn'
    #file_output = './data/lichess_db_standard_rated_2013-01.csv'

    file_src = './data/oct lichess/lichess_db_standard_rated_2021-10.txt'
    #file_output = './data/lichess_db_standard_rated_2021-10.csv'
    file_output = './data/lichess_db_standard_rated_2021-10-subset.txt'

    #file_src = './data/smallsubset.pgn'
    #file_output = 'data/smallsubset.csv'

    parse_pgn(file_src=file_src, file_output=file_output)


if __name__ == "__main__":
    main()

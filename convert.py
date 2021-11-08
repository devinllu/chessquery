import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt

from converter.pgn_data import PGNData

#converts a pgn to a csv file

src = input("enter file source here (type 'n' to skip): ")

if src == 'n':
    src = 'data/smallsubset.pgn'
    #src = 'data/lichess_db_standard_rated_2013-01.pgn'

try:
    pgn_data = PGNData(src)
    result = pgn_data.export()
    result.print_summary()
except():
    print("file source not found")
import lichess as li
import ml

def main():

    # li.save_by_player(username="EricRosen", max=14000, color='white', variant='bullet')
    ml.predict(file='data/lichess-std-big.csv')

if __name__ == "__main__":
    main()